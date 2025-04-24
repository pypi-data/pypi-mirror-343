import json
from typing import Optional, Union, List
from functools import partial
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from EstateEdgePy.src._base_request import BaseRequest
from EstateEdgePy.src.logger import CustomLogger
from EstateEdgePy.src._api_request import AsyncBaseRequest
from EstateEdgePy.src.utils import convert_to_table
from EstateEdgePy.core.filters import filter_sales_price, filter_by_date, filter_property_type, filter_real_estate_type, \
    filter_transfer_type, filter_transfer_price, filter_sales_price_range, filter_min_max_price, filter_location


class PropertiesData:
    _cached_data = None

    def __init__(self):
        self.base_request = BaseRequest()
        self.logger = CustomLogger().logger
        self.client = AsyncBaseRequest(self.base_request, self.logger)

    # UPDATE TO CONSIDER
    """
    - Create a cached method/instance that checks and updates the latest properties from the last update in the database
    - Save method/instance to save properties data
    """


    def get_properties(self):
        if self._cached_data:
            """return properties data that has been cached previously"""
            return self._cached_data

        try:
            data = self.client.fetch_data()

            if data is None:
                return """
                No properties found.
                Please check your API credentials and try again.
                If the issue persists, please contact the API provider.
                """
            self._cached_data = convert_to_table(data)
            return self._cached_data
        except Exception as e:
            self.logger.error(f"Failed to fetch properties: {e}", exc_info=True)
            return {
                "error": "An error occurred while fetching properties.",
                "details": str(e)
            }

    def save(self, file_path: str, file_type: str = "json"):
        """
        Save the cached data in the specified format (JSON, CSV, or Parquet).

        Args:
            file_path (str): The file path where the data will be saved.
            file_type (str): The file format ("json", "csv", "parquet").
        """
        if not self._cached_data:
            self.logger.warning("No data to save. Please fetch data first.")
            return

        try:
            if file_type == "json":
                self._save_as_json(file_path)
            elif file_type == "csv":
                self._save_as_csv(file_path)
            elif file_type == "parquet":
                self._save_as_parquet(file_path)
            else:
                self.logger.error(f"Unsupported file type: {file_type}")
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}", exc_info=True)

    def _save_as_json(self, file_path: str):
        """Helper method to save data as a JSON file."""
        data_dict = self._cached_data.to_pandas().to_dict(orient="records")
        with open(file_path, "w") as f:
            json.dump(data_dict, f, indent=4)
        self.logger.info(f"Data saved as JSON to {file_path}")

    def _save_as_csv(self, file_path: str):
        """Helper method to save data as a CSV file."""
        df = self._cached_data.to_pandas()
        df.to_csv(file_path, index=False)
        self.logger.info(f"Data saved as CSV to {file_path}")

    def _save_as_parquet(self, file_path: str):
        """Helper method to save data as a Parquet file."""
        pq.write_table(self._cached_data, file_path)
        self.logger.info(f"Data saved as Parquet to {file_path}")

    def __repr__(self):
        pass



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


# prop = PropertiesData()
# prop_data = prop.get_properties()
#
# print(prop_data)

# prop.save("data_output.csv", "csv")
# prop_det = PropertyDetail(prop_data)
# sales_price = prop_det.filter(sales_prices="420000", sales_min_value=400000.0)
# print(sales_price.to_pandas())
