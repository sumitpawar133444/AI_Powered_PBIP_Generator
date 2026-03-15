from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class BarChart(BaseChart):
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds)

    def build_projections(self, dimensions: list, measures: list) -> dict:
        """
        Build Power BI projections for Bar Chart.
        Uses new frontend_spec format:
        dimensions -> ["region"]
        measures -> ["revenue"]
        """
        projections = {
            "Category": {"projections": []},
            "Series": {"projections": []},
            "Y": {"projections": []},
            "Tooltips": {"projections": []}
        }

        table = self.visual_definition.get("table")

        for i, dim in enumerate(dimensions):
            proj = self.column_projection(table, dim)

            if i == 0:
                projections["Category"]["projections"].append(proj)
            elif i == 1:
                projections["Series"]["projections"].append(proj)
            else:
                projections["Tooltips"]["projections"].append(proj)

        # Measures → Y
        for measure in measures:

            proj = self.column_aggregation_projection(
                "sum",      # default aggregation
                table,
                measure,
                measure
            )

            projections["Y"]["projections"].append(proj)

        return projections

    # def generate_filter_object(self):
    #     return []

    def generate_visual_specific_properties(self):
        return {}