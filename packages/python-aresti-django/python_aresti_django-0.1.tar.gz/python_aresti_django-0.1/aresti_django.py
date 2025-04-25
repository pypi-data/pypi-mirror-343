''' Aresti-rajapintayhteys Django-testityökalujen kautta.

>>> from dataclasses import dataclass
>>> from django.contrib.auth import get_user_model
>>> from django import test
>>> from aresti import JsonYhteys, RestSanoma
>>> from aresti_django import AsyncClient, DjangoYhteys
>>>
>>> class Yhteys(JsonYhteys, DjangoYhteys):
...   class Rajapinta(DjangoYhteys.Rajapinta):
...     class Meta(DjangoYhteys.Rajapinta.Meta):
...       rajapinta = '/api/rajapinta/'
...     @dataclass
...     class Syote(RestSanoma):
...       kentta: str
...     @dataclass
...     class Tuloste(RestSanoma):
...       id: str
...       kentta: str
>>>
>>> class Testi(test.TestCase):
...   async_client_class = AsyncClient  # Tarvittaessa.
...
...   async def testi(self):
...     self.async_client.force_login(  # Tarvittaessa.
...       get_user_model().objects.first()
...     )
...     async with Yhteys(
...       async_client=self.async_client,  # Tarvittaessa.
...     ) as yhteys:
...       self.assertEqual(
...         (await yhteys.rajapinta.lisaa(kentta='foo')).kentta,
...         'foo',
...       )
'''

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import functools
import json
from typing import ClassVar

from django.test.client import AsyncClient

from aresti import AsynkroninenYhteys


class AsyncClient(AsyncClient):
  ''' Täydennetty asiakasyhteystoteutus. '''
  # pylint: disable=function-redefined

  async def request(self, **request):
    ''' Jäljittele aiohttp.ClientResponse-luokkaa. '''
    sanoma = await super().request(**request)
    sanoma.content_type = sanoma['Content-Type']
    sanoma.status = sanoma.status_code

    async def text(arvo):
      return arvo.decode()
    sanoma.text = functools.partial(text, sanoma.content)

    async def _read(arvo):
      return arvo
    sanoma.read = functools.partial(_read, sanoma.content)

    async def _json(sanoma):
      return json.loads(await sanoma.read())
    sanoma.json = functools.partial(_json, sanoma)

    return sanoma
    # async def request

  def konteksti(self, metodi):
    ''' Kääri HTTP-pyyntö asynkroniseksi kontekstiksi. '''

    @asynccontextmanager
    async def funktio(*args, **kwargs):
      if content_type := kwargs.get('headers', {}).get('Content-Type'):
        # Anna mahdollinen `Content-Type` nimettynä parametrinä.
        if content_type == 'application/x-www-form-urlencoded':
          # Käsittele lomakedata erikseen.
          kwargs['data'] = '&'.join(map('='.join, kwargs['data'].items()))
        kwargs['content_type'] = content_type
      yield await getattr(self, metodi)(*args, **kwargs)
      # async def funktio

    return funktio
    # def konteksti

  # class AsyncClient


@dataclass
class Istunto:
  ''' Käytä Django-testiasiakasta Aiohttp-istuntona. '''
  async_client: AsyncClient

  def __getattr__(self, metodi):
    '''
    Käännetään GET-, POST- jne. pyynnöt testiyhteyden konteksteiksi.
    '''
    return self.async_client.konteksti(metodi)

  # class Istunto


@dataclass
class DjangoYhteys(AsynkroninenYhteys):
  palvelin: ClassVar[str] = 'http://testserver'
  async_client: AsyncClient = field(default_factory=AsyncClient)

  async def __aenter__(self):
    # pylint: disable=attribute-defined-outside-init
    async with self._istunto_lukitus:
      if not (istunto_avoinna := self._istunto_avoinna):
        self._istunto = Istunto(self.async_client)
      self._istunto_avoinna = istunto_avoinna + 1
    return self
    # async def __aenter__

  async def __aexit__(self, *exc_info):
    # pylint: disable=attribute-defined-outside-init
    async with self._istunto_lukitus:
      if not (istunto_avoinna := self._istunto_avoinna - 1):
        del self._istunto
      self._istunto_avoinna = istunto_avoinna
    # async def __aexit__

  # class DjangoYhteys
