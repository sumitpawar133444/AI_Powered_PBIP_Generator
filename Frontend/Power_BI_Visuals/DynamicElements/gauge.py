from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class Gauge(BaseChart):
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, dimension_mapping) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds, dimension_mapping)

    def build_projections(self, dimensions: list, measures: list) -> dict:
        projections = {
            "Y": {"projections": []},           # Main value
            "MinValue": {"projections": []},    # Gauge minimum
            "MaxValue": {"projections": []},    # Gauge maximum
            "TargetValue": {"projections": []}  # Target line
        }

        # Y: First metric (main gauge value)
        if measures:
            measure = measures[0]
            measure_name = measure.get("definition", {}).get("qLabel", "")
            measure_source = measure.get("source", "")
            if measure_source == "library":
                proj = self.measure_projection("measure", measure_name)
            elif measure_source == "inline":
                agg, field_name = self._parse_qlik_measure(measure_name)
                #Update later
                proj = self.column_aggregation_projection(agg, "table", field_name, field_name)

            projections["Y"]["projections"].append(proj)

        return projections

    def generate_visual_specific_properties(self):
        return {}
