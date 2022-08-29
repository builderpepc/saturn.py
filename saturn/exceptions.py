from __future__ import annotations

import asyncio
import aiohttp
import logging
from typing import Optional, List, Mapping, TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from client import Client

class ClientNotReadyError(Exception):
    def __init__(client: Client, message: str = None):
        self.client = client
        self.message = message