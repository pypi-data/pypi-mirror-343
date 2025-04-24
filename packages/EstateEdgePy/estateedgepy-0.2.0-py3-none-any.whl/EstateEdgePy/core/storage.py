import asyncio
import json
from typing import Optional, Union, List
from functools import partial
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from EstateEdgePy.filters.base_filter import BaseFilter
from EstateEdgePy.filters.price_filter import PriceRangeFilter
from EstateEdgePy.src._client import EstateEdgeClient
from EstateEdgePy.src.logger import CustomLogger
from EstateEdgePy.core.filters import filter_sales_price, filter_by_date, filter_property_type, filter_real_estate_type, \
    filter_transfer_type, filter_transfer_price, filter_sales_price_range, filter_min_max_price, filter_location


class PropertyService:
    def __init__(self, client: Optional[EstateEdgeClient] = None) -> None:
        self.client = client or EstateEdgeClient()  # Default client if none provided

    async def get_filtered(
        self,
        state: str,
        filters: Optional[List[BaseFilter]] = None
    ) -> pa.Table:
        raw_data = await self.client.get_property_table(state)
        if filters:
            for filter_item in filters:
                raw_data = filter_item.apply(raw_data)
        return raw_data

    async def to_pandas(self, state: str, columns: Optional[List[str]] = None):
        data = await self.get_filtered(state)
        df = data.to_pandas()
        return df[columns] if columns else df


class PropertyDetail:
    def __init__(self, property_data: pa.Table, logger: CustomLogger = None):
        self.data_table = property_data
        self.logger = logger or CustomLogger().logger

    def to_pandas(self, *columns):
        if not self.data_table:
            return None
        dataframe = self.data_table.to_pandas()
        return dataframe.filter(columns) if len(columns) > 0 else dataframe

    def filter(
            self,
            sales_prices: Union[str, List[str]] = None,
            sales_min_value: float = None,
            sales_max_value: float = None,
            property_type: Union[str, List[str]] = None,
            real_estate_type: Union[str, List[str]] = None,
            date_column: str = None,
            date_range: str = None,
            transfer_type: Union[str, List[str]] = None,
            transfer_price: Union[str, List[str]] = None,
            state: Union[str, List[str]] = None,
            county: Union[str, List[str]] = None,
            street: Union[str, List[str]] = None,
            neighborhood: Union[str, List[str]] = None,
            zipcode: Union[str, List[str]] = None,
            case_sensitive: bool = True,
            is_min_max: bool = False
    ):
        property_data = self.data_table

        # Normalize sales_prices into a list of strings
        if sales_prices:
            sales_prices = self._normalize_input(sales_prices)
            property_data = filter_sales_price(property_data, sales_prices)

        num_properties_sold = property_data.num_rows  # return this or pass it through a function or class or instance or object

        if sales_prices and sales_min_value:
            sales_prices = self._normalize_input(sales_prices)
            property_data = filter_sales_price_range(property_data, sales_prices, min_price=sales_min_value)

        if sales_prices and sales_max_value:
            sales_prices = self._normalize_input(sales_prices)
            property_data = filter_sales_price_range(property_data, sales_prices, max_price=sales_max_value)

        if is_min_max:
            property_data = filter_min_max_price(property_data, date_column)  # filter any column price for min and max prices

        if property_type:
            property_type = self._normalize_input(property_type)
            property_data = filter_property_type(property_data, property_type)

        if real_estate_type:
            real_estate_type = self._normalize_input(real_estate_type)
            property_data = filter_real_estate_type(property_data, real_estate_type)

        if state and county or street or neighborhood or zipcode:
            state_type = self._normalize_input(state)
            county_type = self._normalize_input(county)
            street_type = self._normalize_input(street)
            neighborhood_type = self._normalize_input(neighborhood)
            zipcode_type = self._normalize_input(zipcode)
            property_data = filter_location(property_data, state_type, county_type, street_type, neighborhood_type, zipcode_type, case_sensitive)

        if date_column and date_range:
            property_data = filter_by_date(property_data, date_range, date_column)

        if transfer_type:
            transfer_type = self._normalize_input(transfer_type)
            property_data = filter_transfer_type(property_data, transfer_type)

        if transfer_price:
            transfer_price = self._normalize_input(transfer_price)
            property_data = filter_transfer_price(property_data, transfer_price)

        return PropertyDetail(property_data)

    @staticmethod
    def _normalize_input(input_data: Union[str, List[str]]) -> List[str]:
        """Helper function to normalize input into a list of strings."""
        if isinstance(input_data, str):
            return [input_data]
        elif isinstance(input_data, list):
            return list(map(str, input_data))
        return []
