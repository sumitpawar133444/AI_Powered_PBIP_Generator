from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class KPI(BaseChart):
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, dimension_mapping) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds, dimension_mapping)

    def build_projections(self, dimensions: list, measures: list) -> dict:
        projections = {
            "Data": {"projections": []},    # Main KPI value
            "Rows": {"projections": []}     # Trend axis (time/category)
        }

        if measures:
            measure = measures[0]
            measure_name = measure.get("definition", {}).get("qLabel", "")
            measure_source = measure.get("source", "")

            # Use aggregation projection for measures
            if measure_source == "library":
                proj = self.measure_projection("measure", measure_name)
            elif measure_source == "inline":
                agg, field_name = self._parse_qlik_measure(measure_name)
                #Update later
                proj = self.column_aggregation_projection(agg, "table", field_name, field_name)


            projections["Data"]["projections"].append(proj)

        if dimensions:
            dim = dimensions[0]
            field_name = dim.get("definition", {}).get("qDef", {}).get("qFieldDefs", [None])[0]

            if field_name:
                table = self.dimension_mp.get(field_name)
                projections["Rows"]["projections"].append(
                    self.column_projection(table, field_name)
                )

        return projections

    def generate_visual_specific_properties(self):
        return {}
