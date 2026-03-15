from Frontend.Power_BI_Models.visualConatiner_2_2_0 import VisualContainer1, VisualContainerPosition
from Frontend.Power_BI_Models.visualConfiguration_2_2_0 import VisualConfiguration, VisualContainerFormattingObjects, Title
from Frontend.Power_BI_Models.formattingObjectsDefinitions_1_4_0 import DataViewObjectDefinitions
from Frontend.Power_BI_Models.filterConfiguration_1_2_0 import FilterConfiguration


class BaseVisual:
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds):
        BASE_WIDTH = 1280
        BASE_HEIGHT = 720
        self.visual_id = visual_id
        self.visual_type = visual_type
        self.data = visual_defintion
        self.visual_bounds = visual_bounds
        self.page_width = BASE_WIDTH- 10
        self.page_height = BASE_WIDTH- 10
        self.query_data_needed = True
        self.visual_type = self.generate_visual_type()
        # self.is_chart = data.get('is_chart', False)

    def generate_visual(self):
        data = self.data
        field_schema = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.2.0/schema.json'

        position = self.generate_visual_position()

        visual = VisualConfiguration(visualType = self.visual_type)
        # visual.visualContainerObjects = BaseVisualContainerFormattingObjects(item, self.visual_type).generate_visualContainerFormattingObjects()
        visual.drillFilterOtherVisuals = True
        if self.query_data_needed :
            visual.query = self.generate_visual_query()

        objects = DataViewObjectDefinitions()
        chart_specific_properties = self.generate_chart_properties()
        visual_specific_properties = self.generate_visual_specific_properties()
        objects.root = {**chart_specific_properties, **visual_specific_properties}
        visual.objects = objects

        filter_factory = FilterConfiguration()
        filter_factory.filters = self.generate_filter_object()

        return VisualContainer1(
                name = self.visual_id,
                field_schema = field_schema,
                position = position,
                visual = visual,
                filterConfig = filter_factory
            )


    def generate_filter_object(self):
        raise NotImplementedError

    def generate_visual_type(self):
        visual_map = {
            "barchart": "columnChart",
            "linechart": "lineChart",
            "kpi": "cardVisual",
            "gauge": "gauge",
            "treemap": "treemap"
        }
        return visual_map.get(self.visual_type, self.visual_type)

    def get_x_and_y(self):
        # 5 is due to page margin and 2 is margin inside grid
        bounds = self.visual_bounds
        x = ((bounds["x"] / 100) * self.page_width) + 5 + 2
        y = ((bounds["y"] / 100) * self.page_height) + 5 + 2
        return x, y

    def get_width_and_height(self):
        # 4 is due to margin_left and margin_right
        bounds = self.visual_bounds
        width = ((bounds["width"] / 100) * self.page_width) - 4
        height = ((bounds["height"] / 100) * self.page_height) - 4
        return width, height

    def generate_visual_position(self):
        x, y = self.get_x_and_y()
        width, height = self.get_width_and_height()
        try:
            visualContainerPosition = VisualContainerPosition(
                x = x,
                y = y,
                width = width,
                height = height
            )

        except Exception as e:
            print(e)
        return visualContainerPosition

    def _get_entity_from_attribute(self, attr_info: dict) -> str:
        """Extract datasetName as entity from {name, datasetName}"""
        dataset_name = attr_info.get("datasetName", "UnknownDataset")
        return dataset_name

    def column_projection(self, table: str, col: str) -> dict:
        return {
            "field": {
                "Column": {
                    "Expression": {"SourceRef": {"Entity": table}},
                    "Property": col
                }
            },
            "queryRef": f"{table}.{col}",
            "nativeQueryRef": col,
            "active": True
        }

    def measure_projection(self, table: str, col: str) -> dict:
        return {
            "field": {
                "Measure": {
                    "Expression": {"SourceRef": {"Entity": table}},
                    "Property": col
                }
            },
            "queryRef": f"{table}.{col}",
            "nativeQueryRef": col,
            "active": True
        }

    def column_aggregation_projection(self, agg: str, table: str, col: str, display_name: str | None = None) -> dict:
        #display_name for future implementation
        agg_function_map = {
            "Sum": 0,
            "Avg": 1,
            "Average": 1,
            "Min": 2,
            "Max": 3,
            "Count": 4,
            "CountDistinct": 5,
            "Median": 6,
            "StDev": 7,
            "StDevP": 7,
            "Var": 8,
            "VarP": 8,
            "First": 9,
            "Last": 10,
            "RangeAvg": 11,
            "RangeSum": 12,
            "RankSum": 13,
            "RankAvg": 14,
            "RankMin": 15,
            "RankMax": 16,
            "Rank": 17,
            "CumSum": 18,
            "CumProd": 19,
            "RangeCount": 20,
            "RangeSumAvg": 21,
            "N": 22,
            "NoOfRows": 23,
            "Above": 24,
            "Below": 25,
            "Total": 26
        }
        display = display_name or col
        func_code = agg_function_map.get(agg, 0)
        return {
            "field": {
                "Aggregation": {
                    "Expression": {
                        "Column": {
                            "Expression": {"SourceRef": {"Entity": table}},
                            "Property": col
                        }
                    },
                    "Function": func_code
                }
            },
            "queryRef": f"{agg}({table}.{col})",
            "nativeQueryRef": display,
            "displayName": display
        }

    def generate_visual_query(self):
        """Generate grid projections using Rows, Columns, Values wells"""
        return {
            "queryState": self.build_projections(
                dimensions=self.data.get("qDimensions", []),
                measures=self.data.get("qMeasures", [])
            )
        }

    def set_themes(self, themes):
        self.themes = themes
