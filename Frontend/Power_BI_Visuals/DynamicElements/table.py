from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class PivotTable(BaseChart):
    def __init__(self, item) -> None:
        super().__init__(item)

    def build_projections(self, rowAttributes: list, columnAttributes: list, metrics: list) -> dict:
        """Build grid-specific wells: Rows, Columns, Values"""
        projections = {
            "Rows": {"projections": []},
            "Columns": {"projections": []},
            "Values": {"projections": []}
        }

        # Rows: rowAttributes (grid rows/hierarchy)
        for attr in rowAttributes:
            entity = self._get_entity_from_attribute(attr)
            projections["Rows"]["projections"].append(
                self.make_column_and_row_projection(entity, attr["name"])
            )

        # Columns: columnAttributes (grid columns)
        for attr in columnAttributes:
            entity = self._get_entity_from_attribute(attr)
            projections["Columns"]["projections"].append(
                self.make_column_and_row_projection(entity, attr["name"])
            )

        # Values: all metrics (grid measures)
        for metric in metrics:
            entity = self._get_entity_from_attribute(metric)
            projections["Values"]["projections"].append(
                self.make_metric_agg_projection(entity, metric["name"], metric["name"])
            )

        return projections


    def generate_filter_object(self):
        """Generate filters array for columnNames and Metrics"""
        dataset = self.item.get('dataSet', 'DataSet')  # Fallback to 'DataSet' if not found

        filters = []

        # Process columnNames for Categorical filters
        column_names = self.item.get('columnNames', [])
        for i, col_name in enumerate(column_names):
            filter_obj = {
                "name": f"col_filter_{i}",
                "field": {
                    "Column": {
                        "Expression": {
                            "SourceRef": {
                                "Entity": dataset
                            }
                        },
                        "Property": col_name
                    }
                },
                "type": "Categorical"
            }
            filters.append(filter_obj)

        # Process Metrics for Advanced filters
        metrics = self.item.get('metrics', [])
        for i, metric in enumerate(metrics):
            filter_obj = {
                "name": f"metric_filter_{i}",
                "field": {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {
                                    "SourceRef": {
                                        "Entity": dataset
                                    }
                                },
                                "Property": metric
                            }
                        },
                        "Function": 0
                    }
                },
                "type": "Advanced"
            }
            filters.append(filter_obj)

        return filters


    def generate_visual_specific_properties(self):
        return {}