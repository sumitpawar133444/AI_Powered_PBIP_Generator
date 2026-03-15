# Core/utils.py
import os
import ssl
import uuid
import numpy as np
import pandas as pd

def bypass_ssl():
    """Fixes SSL certificate issues for Gemini API."""
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass

class GuidRegistry:
    """Manages UUIDs for PBI objects and relationships."""
    def __init__(self):
        self.date_variations = {}
        self.data_relationships = []

    def get_new_guid(self) -> str:
        return str(uuid.uuid4())

    def register_date_column(self, table_name: str, column_name: str):
        key = (table_name, column_name)
        if key not in self.date_variations:
            self.date_variations[key] = {
                "relationship_guid": self.get_new_guid(),
                "local_table_guid": self.get_new_guid(),
                "local_table_name": f"LocalDateTable_{self.get_new_guid()}",
                "date_hierarchy_guid": self.get_new_guid()
            }
        return self.date_variations[key]

    def register_data_relationship(self, from_table, from_col, to_table, to_col):
        self.data_relationships.append({
            "guid": self.get_new_guid(),
            "from_table": from_table,
            "from_col": from_col,
            "to_table": to_table,
            "to_col": to_col
        })


class DataSimulator:
    """Generates dummy data for the Streamlit preview."""
    @staticmethod
    def get_mock_data(visual_type, columns):
        v_type = str(visual_type).lower() if visual_type else 'card'
        cols = columns if columns else ["Value"]
        if v_type == 'card':
            return np.random.randint(1000, 99999)

        # Standardize dummy dataframe generation
        df = pd.DataFrame(np.random.randn(10, len(cols)), columns=cols)
        df['Category'] = [f"Item {i}" for i in range(10)]
        return df.set_index('Category')