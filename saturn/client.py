import asyncio
import aiohttp
import logging
from typing import List, Mapping, Callable, Coroutine, Optional, Union
import datetime
import json

import endpoints
from models import User, ClientUser

class Client:
    def __init__(self, access_token: str, refresh_token: str, token_refresh_interval: Union[datetime.timedelta, float, int] = datetime.timedelta(hours=2)):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_refresh_interval = token_refresh_interval if not isinstance(token_refresh_interval, datetime.timedelta) else token_refresh_interval.total_seconds()
        self.loop = asyncio.new_event_loop()
        self.session: Optional[aiohttp.ClientSession] = None
        self._logger = logging.getLogger('client')
        self.chats: List[Chat] = []
        self.event_handlers: Mapping[str, List[Callable]] = {k: [] for k in [
            'ready',
            'message',
            'error',
            'token_refresh',
            'start'
        ]}

        self._default_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json;charset=utf-8"
        }

        self._ready_dispatched = False

        self.user: Optional[ClientUser] = None
        self.event_handlers['token_refresh'].append(self.fetch_self)
    

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def token_refresh_interval(self) -> Union[float, int]:
        return self._token_refresh_interval

    @property
    def _authorization_header(self) -> str:
        return "Bearer " + self._access_token
    
    def run(self):
        try:
            self.loop.create_task(self.start())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            asyncio.run(self.close())

    async def start(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.loop.create_task(self.token_refresh_cycle())
        await self.dispatch('start')
        
    async def token_refresh_cycle(self):
        while not self.loop.is_closed():
            await self.request_refresh_token()
            await asyncio.sleep(self.token_refresh_interval)

    async def request_refresh_token(self):
        self._logger.debug("Attempting token refresh.")
        async with self.session.post(
            endpoints.REFRESH_AUTH,
            headers=self._default_headers,
            data=json.dumps({
                "access_token": self.access_token,
                "refresh_token": self.refresh_token
            })
        ) as res:
            res.raise_for_status()
            data = await res.json()
            if data['access_token']:
                self._access_token = data['access_token']
            if data['refresh_token']:
                self._refresh_token = data['refresh_token']
            await self.dispatch('token_refresh')
            
    async def _request(self, endpoint_url: str):
        async with self.session.get(
            endpoint_url,
            headers=(self._default_headers | {"Authorization": self._authorization_header}),
        ) as res:
            res.raise_for_status()
            return await res.json()

    async def fetch_self(self) -> ClientUser:
        self.user = ClientUser(await self._request(endpoints.ME), session=self.session)
        if not self._ready_dispatched: # fetch_self is called each token refresh, so we can check for the first refresh here
            self._ready_dispatched = True
            await self.dispatch('ready') # this way, ready is only dispatched once self.user is loaded
        return self.user

    async def close(self):
        await self.session.close()
        self.loop.close()

    async def dispatch(self, event: str):
        self._logger.debug(f"Dispatching event '{event}'")
        if event in self.event_handlers.keys():
            await asyncio.gather(*[x() for x in self.event_handlers[event]])

    def on(self, event: str):
        def ret(func: Callable):
            self.event_handlers[event].append(func)
            return func
        return ret

if __name__ == '__main__':
    from rich import print

    bot = Client(
        '***REMOVED***',
        '***REMOVED***'
    )

    @bot.on("start")
    async def on_start():
        print("Saturn bot started")

    @bot.on("ready")
    async def on_ready():
        print("Connected successfully")
        print("Name: " + bot.user.name)
        print("Created at: " + str(bot.user.created_at))

    bot.run()