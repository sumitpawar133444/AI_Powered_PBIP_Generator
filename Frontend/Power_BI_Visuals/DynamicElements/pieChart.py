from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class PieChart(BaseChart):
    def __init__(self, item) -> None:
        super().__init__(item)

    def build_projections(self, rowAttributes: list, columnAttributes: list, metrics: list) -> dict:
        projections = {
            "Category": {"projections": []},
            "Series": {"projections": []},
            "Y": {"projections": []},
            "Tooltips": {"projections": []}
        }

        # Category: columnAttributes → read datasetName directly
        for attr in rowAttributes:
            entity = self._get_entity_from_attribute(attr)  # Gets "SalesData"
            projections["Category"]["projections"].append(
                self.make_column_and_row_projection(entity, attr["name"])  # SalesData.Product
            )

        # Series: rowAttributes → read datasetName directly
        for attr in columnAttributes:
            entity = self._get_entity_from_attribute(attr)  # Gets "BU_Infoo"
            projections["Series"]["projections"].append(
                self.make_column_and_row_projection(entity, attr["name"])  # BU_Infoo.Bu_Key
            )

        # Y: first metric → read datasetName directly
        if metrics:
            first_metric = metrics[0]
            entity = self._get_entity_from_attribute(first_metric)  # Gets "BU_Infoo"
            projections["Y"]["projections"].append(
                self.make_metric_agg_projection(entity, first_metric["name"], first_metric["name"])
            )

        # Tooltips: all metrics → read datasetName directly
        for metric in metrics[1:]:
            entity = self._get_entity_from_attribute(metric)  # Gets datasetName for each
            projections["Tooltips"]["projections"].append(
                self.make_metric_agg_projection(entity, metric["name"], metric["name"])
            )

        return projections


    # def generate_filter_object(self):
    #     return []

    def generate_visual_specific_properties(self):
        return {}