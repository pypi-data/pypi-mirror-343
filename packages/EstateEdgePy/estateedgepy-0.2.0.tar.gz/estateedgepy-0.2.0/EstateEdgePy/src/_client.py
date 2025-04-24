import aiohttp
import asyncio
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import pyarrow as pa

from EstateEdgePy.src.logger import CustomLogger
from EstateEdgePy.src.constants import PROPERTIES_URL, BASE_URL
from EstateEdgePy.src.utils import convert_to_table


class EstateEdgeClient:
    def __init__(self) -> None:
        self.base_url: str = BASE_URL
        self._headers: dict = {"Accept": "application/json"}
        self._logger = CustomLogger()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(aiohttp.ClientError),
        reraise=True,
    )
    async def get_property_table(self, state: str) -> pa.Table:
        """Fetch full property dataset and convert to PyArrow Table."""
        url = f"{self.base_url.rstrip('/')}/{PROPERTIES_URL.lstrip('/')}"

        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(url, params={"state": state}) as response:
                response.raise_for_status()
                data: List[Dict[str, Any]] = await response.json()
                return convert_to_table(data)
