from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class BarChart(BaseChart):
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping)

    def build_projections(self, dimensions: list, measures: list) -> dict:
        projections = {
            "Category": {"projections": []},
            "Series": {"projections": []},
            "Y": {"projections": []},
            "Tooltips": {"projections": []}
        }

        for i, dim in enumerate(dimensions):
            field_name = dim.get("definition", {}).get("qDef", {}).get("qFieldDefs", [None])[0]
            table = self.dimension_mp.get(field_name)

            proj = self.column_projection(table, field_name)

            if i == 0:
                projections["Category"]["projections"].append(proj)
            elif i == 1:
                projections["Series"]["projections"].append(proj)
            else:
                projections["Tooltips"]["projections"].append(proj)

        # Measures → Y
        for measure in measures:
            measure_name = measure.get("definition", {}).get("qLabel", "")
            measure_source = measure.get("source", "")

            # Use aggregation projection for measures
            if measure_source == "library":
                proj = self.measure_projection("measure", measure_name)
            elif measure_source == "inline":
                agg, field_name = self._parse_qlik_measure(measure_name)
                #Update later
                proj = self.column_aggregation_projection(agg, "table", field_name, field_name)

            projections["Y"]["projections"].append(proj)

        return projections

    # def generate_filter_object(self):
    #     return []

    def generate_visual_specific_properties(self):
        return {}