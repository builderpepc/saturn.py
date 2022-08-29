from __future__ import annotations

import asyncio
import aiohttp
import logging
from typing import Optional, List, Mapping, TYPE_CHECKING
import datetime
import copy

from models import BaseUser, User
from exceptions import ClientNotReadyError

if TYPE_CHECKING:
    from client import Client

class UserCache:
    def __init__(self, client: Client, registry: dict = {}):
        self.client = client
        self._registry: Mapping[int, dict] = registry

    def __getitem__(self, key: int) -> Optional[User]:
        ret = self._registry.get(key)
        if ret:
            ret = ret['user']
        return ret

    def update_many(self, data: List[dict]):
        # For raw data from /users
        for x in data:
            [self.update_user(x) for x in data]

    def update_user(self, data: dict):
        if not self.client.ready:
            raise ClientNotReadyError(self.client, "Attempted to modify the user cache, but the given Client does not seem to have connected yet.")
        
        user_id = data['id']

        if user_id not in self._registry.keys():
            self._registry[user_id] = {
                'updated': datetime.datetime.now(),
                'user': User(data)
            }
        else:
            self._registry[user_id] = datetime.datetime.now()
            self._registry['user'].update(data)

    def to_dict(self) -> dict:
        return copy.copy(self._registry)