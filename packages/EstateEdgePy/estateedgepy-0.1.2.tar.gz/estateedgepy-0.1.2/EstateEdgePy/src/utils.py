from typing import List, Dict, Any

import pyarrow as pa
import pandas as pd


# Define the PyArrow schema
schema = pa.schema([
    ("street_location", pa.string()),
    ("account_identifier", pa.string()),
    ("grantee", pa.string()),
    ("property_type", pa.string()),
    ("stories", pa.string()),
    ("year_built", pa.string()),  # Converting to float for consistency
    ("quality", pa.string()),  # Converting to float
    ("living_area", pa.string()),  # Keeping as string due to 'SF' suffix
    ("land_area", pa.string()),  # Keeping as string due to 'AC' suffix
    ("transfer_date", pa.string()),  # Keeping as string to retain date format
    ("sale_price", pa.string()),  # Converting to integer
    ("county", pa.string()),
    ("state", pa.string()),
    ("data_retrieval_date", pa.string()),
    ("real_estate_type", pa.string()),
    ("account_id_expanded", pa.string()),
    ("district", pa.string()),  # Converting to float
    ("account_number", pa.string()),  # Converting to float
    ("owner_name", pa.string()),
    ("mailing_address", pa.string()),
    ("premise_address", pa.string()),
    ("zip_code", pa.string()),
    ("map", pa.string()),
    ("grid", pa.string()),  # Converting to float
    ("parcel", pa.string()),  # Converting to float
    ("neigborhood", pa.string()),  # Keeping as string to prevent loss of precision
    ("subdivision", pa.string()),  # Converting to float
    ("section", pa.string()),  # Keeping as string (empty values)
    ("block", pa.string()),  # Keeping as string (empty values)
    ("lot", pa.string()),  # Keeping as string since it may contain non-numeric values
    ("assessment_year", pa.string()),  # Converting to float
    ("base_value_land", pa.string()),  # Converting to float
    ("base_value_improvements", pa.string()),  # Converting to float
    ("town", pa.string()),  # Keeping as string due to NaN values
    ("base_value_total", pa.string()),  # Converting to float
    ("phase_in_assessments1", pa.string()),  # Converting to float
    ("phase_in_assessments2", pa.string()),  # Converting to float
    ("assessment_date1", pa.string()),  # Keeping as string to retain date format
    ("assessment_date2", pa.string()),  # Keeping as string to retain date format
    ("seller", pa.string()),
    ("sale_date", pa.string()),  # Keeping as string to retain date format
    ("price_transfer_info", pa.string()),  # Converting to float
    ("type_transfer_info", pa.string()),
    ("deed_transfer_info", pa.string()),
    ("deed2_transfer_info", pa.string())  # Keeping as string due to NaN values
])


def convert_to_table(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Get the properties"""
    # Your implementation here
    data = pa.Table.from_pylist(data, schema=schema)
    return data
