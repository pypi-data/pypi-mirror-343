import asyncio
import random
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from aiohttp import ClientTimeout, ClientError, ContentTypeError

from EstateEdgePy.src.constants import BASE_URL



class AbstractHTTPClient(ABC):
    @abstractmethod
    async def fetch(self, endpoint: str, **kwargs):
        pass


class BaseRequest(AbstractHTTPClient):
    def __init__(self, base_url: str = BASE_URL) -> None:
        self._base_url: str = base_url
        self._timeout: ClientTimeout = ClientTimeout(total=60)
        self._session = None

    async def fetch(
            self,
            endpoint: str,
            headers: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            retries: int = 3
    ) -> None:
        headers = headers or {}  # Ensure headers are not None
        last_error = None

        for attempt in range(retries):
            try:
                async with self._session.get(f"{self._base_url}{endpoint}", header=headers, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            except (ClientError, ContentTypeError) as error:
                last_error = error
                if attempt == retries - 1:
                    raise last_error
                backoff = (2 ** attempt) + random.uniform(0, 0.5)
                await asyncio.sleep(backoff)
        raise ConnectionError(f"Request failed after {retries} attempts") from last_error

    async def close(self):
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()



