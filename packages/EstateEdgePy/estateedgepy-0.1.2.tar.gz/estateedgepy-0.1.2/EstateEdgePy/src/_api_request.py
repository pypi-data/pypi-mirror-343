import asyncio

from EstateEdgePy.src._base_request import AbstractHTTPClient
from EstateEdgePy.src.logger import CustomLogger
from EstateEdgePy.src._errors import PyRealtyErrors
from EstateEdgePy.src.constants import PROPERTIES_URL


class AsyncBaseRequest:
    def __init__(self, http_client: AbstractHTTPClient, logger: CustomLogger) -> None:
        self._http_client = http_client
        self._logger = logger

    async def _fetch_data(self):
        try:
            response_data = await self._http_client.fetch(PROPERTIES_URL)
            self._logger.info("Fetched data successfully")
            return response_data
        except Exception as error:
            self._logger.error(f"Request failed with error: {error}")
            raise PyRealtyErrors(message=str(error))
            # you can add other exceptions here

    def fetch_data(self):
        """Synchronous wrapper around the _make_request method"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None # No active loop

        if loop and loop.is_running():
            # If there's an event loop (e.g., inside FastAPI), run in a new task
            future = asyncio.create_task(self._fetch_data())
            return future
        else:
            return asyncio.run(self._fetch_data())
