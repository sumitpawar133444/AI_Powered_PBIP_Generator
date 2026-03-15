from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class ComparisonKPI(BaseChart):
    def __init__(self, item) -> None:
        super().__init__(item)

    def build_projections(self, rowAttributes: list, columnAttributes: list, metrics: list) -> dict:
        projections = {
            "Data": {"projections": []},    # Main KPI value
            "Rows": {"projections": []}     # Trend axis (time/category)
        }

        # Data: First metric (KPI value)
        if metrics:
            first_metric = metrics[0]
            entity = self._get_entity_from_attribute(first_metric)
            projections["Data"]["projections"].append(
                self.make_metric_agg_projection(entity, first_metric["name"], first_metric["name"])
            )

        # Rows: First rowAttribute or columnAttribute for trend
        attrs = rowAttributes or columnAttributes
        if attrs:
            first_trend = attrs[0]
            entity = self._get_entity_from_attribute(first_trend)
            projections["Rows"]["projections"].append(
                self.make_column_and_row_projection(entity, first_trend["name"])
            )

        return projections

    def generate_visual_specific_properties(self):
        return {}
