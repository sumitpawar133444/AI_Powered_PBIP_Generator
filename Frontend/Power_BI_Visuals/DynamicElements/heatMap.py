from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class HeatMap(BaseChart):
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping)

    def build_projections(self, dimensions: list, measures: list) -> dict:
        projections = {
            "Group": {"projections": []},
            "Details": {"projections": []},
            "Values": {"projections": []},
            "Tooltips": {"projections": []},
        }

        for i, dim in enumerate(dimensions):
            field_name = dim.get("definition", {}).get("qDef", {}).get("qFieldDefs", [None])[0]

            if not field_name:
                continue

            table = self.dimension_mp.get(field_name)

            if i == 0:
                # First dimension → Group (Y-axis)
                projections["Group"]["projections"].append(
                    self.column_projection(table, field_name)
                )
            elif i == 1:
                # Second dimension → Details (X-axis)
                projections["Details"]["projections"].append(
                    self.column_projection(table, field_name)
                )
            else:
                # Remaining dimensions → Could go to Group/Details as needed; here we put in Group
                projections["Group"]["projections"].append(
                    self.column_projection(table, field_name)
                )

        for j, measure in enumerate(measures):
            measure_name = measure.get("definition", {}).get("qLabel", "")
            measure_source = measure.get("source", "")
            if measure_source == "library":
                proj = self.measure_projection("measure", measure_name)
            elif measure_source == "inline":
                agg, field_name = self._parse_qlik_measure(measure_name)
                #Update later
                proj = self.column_aggregation_projection(agg, "table", field_name, field_name)

            if j == 0:
                # First measure → Values
                projections["Values"]["projections"].append(proj)
            else:
                # Remaining measures → Tooltips
                projections["Tooltips"]["projections"].append(proj)

        return projections

    # def generate_filter_object(self):
    #     return []

    def generate_visual_specific_properties(self):
        return {}