from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class MultiMetricKPI(BaseChart):
    def __init__(self, item) -> None:
        super().__init__(item)

    def build_projections(self, rowAttributes: list, columnAttributes: list, metrics: list) -> dict:
        projections = {
            "Data": {"projections": []},    # ALL metrics as KPI values
            "Rows": {"projections": []}     # Trend axis (optional)
        }

        # Data: ALL metrics (Multi Metric KPI)
        for metric in metrics:
            entity = self._get_entity_from_attribute(metric)
            projections["Data"]["projections"].append(
                self.make_metric_agg_projection(entity, metric["name"], metric["name"])
            )

        # Rows: First rowAttribute or columnAttribute for trend (optional)
        attrs = rowAttributes or columnAttributes
        if attrs:
            first_trend = attrs[0]
            entity = self._get_entity_from_attribute(first_trend)
            projections["Rows"]["projections"].append(
                self.make_column_and_row_projection(entity, first_trend["name"])
            )

        return projections

    def generate_visual_specific_properties(self):
        """Multi Metric KPI formatting."""
        return {
            "dataLabels": {
                "show": True,
                "labelColor": {"solid": {"color": "#FFFFFF"}},
                "fontSize": 18,
                "showSeriesName": True
            },
            "categoryLabels": {
                "show": True,
                "fontSize": 12
            },
            "kpiOptions": {
                "showTrend": True,
                "trendLine": {
                    "show": True,
                    "lineColor": {"solid": {"color": "#666666"}}
                }
            },
            "layout": {
                "displayMode": "multiRow",  # Multiple KPI cards
                "cardSpacing": 10
            }
        }
