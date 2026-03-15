from Frontend.Power_BI_Models.visualConatiner_2_2_0 import VisualContainer1, VisualContainerPosition
from Frontend.Power_BI_Models.visualConfiguration_2_2_0 import VisualConfiguration, VisualContainerFormattingObjects, Title
from Frontend.Power_BI_Models.formattingObjectsDefinitions_1_4_0 import DataViewObjectDefinitions
from Frontend.Power_BI_Models.filterConfiguration_1_2_0 import FilterConfiguration


class BaseVisual:
    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping):
        self.dimension_mp = dimension_mapping
        BASE_WIDTH = 1280
        BASE_HEIGHT = 591
        self.visual_id = visual_id
        self.visual_type = visual_type
        self.data = visual_defintion
        self.visual_bounds = visual_bounds
        self.page_width = BASE_WIDTH- 10
        self.page_height = ((float(sheet_height) / 100.0) * BASE_HEIGHT) - 10
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
                dimensions=self.data.get('qHyperCubeDef', {}).get("qDimensions", []),
                measures=self.data.get('qHyperCubeDef', {}).get("qMeasures", [])
            )
        }

    def set_themes(self, themes):
        self.themes = themes


# class BaseVisualContainerFormattingObjects:
#     def __init__(self, data, visual_type):
#         self.data = data
#         self.visual_type = visual_type
#         # self.is_chart = item.get('is_chart', False)

#     def generate_visual_title(self):
#         data = self.data

#         if data["properties"]["showTitles"]:
#             title_content = data["properties"]["title"]
#             title = Title()
#             title.show = {
#                 "expr": {
#                     "Literal": {
#                         "Value": str(title_details.get("show", True)).lower()
#                     }
#                 }
#             }
#             title.text = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": f" ' {title_content} ' "
#                                 }
#                             }
#                         }

#             title.fontFamily = {
#                                 "expr": {
#                                     "Literal": {
#                                         "Value": f"'Segoe UI'"
#                                     }
#                                 }
#                             }

#             title.fontSize = {
#                                 "expr": {
#                                     "Literal": {
#                                         "Value": str(title_details.get("font_size", "8"))
#                                     }
#                                 }
#                             }

#             title.bold = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": str(title_details.get("is_bold", False)).lower()
#                                 }
#                             }
#                         }

#             title.italic = {
#                                 "expr": {
#                                     "Literal": {
#                                         "Value": str(title_details.get("is_italic", False)).lower()
#                                     }
#                                 }
#                             }

#             title.underline = {
#                                 "expr": {
#                                     "Literal": {
#                                         "Value": str(title_details.get("is_underline", False)).lower()
#                                     }
#                                 }
#                             }

#             title.fontColor = {
#                                 "solid": {
#                                     "color": {
#                                         "expr": {
#                                             "Literal": {
#                                                 "Value": f"'{title_details.get('font_color', '#4e79a7')}'"
#                                             }
#                                         }
#                                     }
#                                 }
#                             }

#             # Add title background functionality
#             title_background = title_details.get('title_background', {})
#             # if self.visual_type == "textbox":
#             #     title_background = {
#             #         'has_background': True,
#             #         'background_color': '#F0F0F0',
#             #         'background_transparency': '0.1D'
#             #     }
#             if title_background.get('has_background', False):
#                 title.background = {
#                     "solid": {
#                         "color": {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": f"'{title_background.get('background_color', '#FFFFFF')}'"
#                                 }
#                             }
#                         }
#                     }
#                 }
#                 # Note: transparency is part of the background object in PowerBI
#                 if title_background.get('background_transparency'):
#                     title.background["transparency"] = {
#                         "expr": {
#                             "Literal": {
#                                 "Value": title_background.get('background_transparency', '0D')
#                             }
#                         }
#                     }

#             title_section = [
#                 {
#                     "properties": title
#                 }
#             ]

#         else:
#             title_section  =[]

#         return title_section

#     def generate_background_section(self):
#         item = self.item
#         background_properties = get_nested_value(item, ['visual_container', 'background_properties'], {})
#         if background_properties.get('has_background') == False:
#             return None

#         if self.visual_type == "textbox":
#             background_section = [
#                 {
#                     "properties": {
#                         "show": {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": "true"
#                                 }
#                             }
#                         },
#                         "color": {
#                             "solid": {
#                                 "color": {
#                                     "expr": {
#                                         "ThemeDataColor": {
#                                             "ColorId": 0,
#                                             "Percent": 0
#                                         }
#                                     }
#                                 }
#                             }
#                         },
#                         "transparency": {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": "100D"
#                                 }
#                             }
#                         }
#                     }
#                 }
#             ]
#         else:
#             background = Background()
#             background.color = {
#                                 "solid": {
#                                     "color": {
#                                         "expr": {
#                                             "Literal": {
#                                                 "Value": f"'{background_properties.get('background_color', '#FFFFFF')}'"
#                                             }
#                                         }
#                                     }
#                                 }
#                             }
#             background.transparency = {
#                                         "expr": {
#                                             "Literal": {
#                                                 "Value": background_properties.get('background_transparency', '0D')
#                                             }
#                                         }
#                                     }
#             background_section = [
#                 {
#                     "properties": background
#                 }
#             ]
#         return background_section

#     def generate_border_section(self):
#         item = self.item
#         border_properties = get_nested_value(item, ['visual_container', 'border_padding', 'border_properties'], {})
#         border = Border()
#         border.show = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": str(border_properties.get("is_present", True)).lower()
#                                 }
#                             }
#                         }

#         border.color = {
#                             "solid": {
#                                 "color": {
#                                     "expr": {
#                                         "Literal": {
#                                             "Value": str(border_properties.get("is_present","")).lower()
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#         border.width = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": str(border_properties.get("border_width", "1")) + "D"
#                                 }
#                             }
#                         }
#         border_section = [
#             {
#                 "properties": border
#             }
#         ]
#         return border_section

#     def generate_padding_section(self):
#         item = self.item
#         padding_properties = get_nested_value(item, ['visual_container', 'border_padding', 'padding_properties'], {})
#         padding = Padding()
#         padding.left = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": padding_properties.get("margin_left", "")
#                                 }
#                             }
#                         }
#         padding.right = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": padding_properties.get("margin_right", "")
#                                 }
#                             }
#                         }
#         padding.bottom = {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": padding_properties.get("margin_bottom", "")
#                                 }
#                             }
#                         }
#         padding.top = {
#                         "expr": {
#                             "Literal": {
#                                 "Value": padding_properties.get("margin_top", "")
#                             }
#                         }
#                     }
#         padding_section = [
#             {
#                 "properties": padding
#             }
#         ]
#         return padding_section

#     def generate_visual_link(self):
#         item = self.item
#         action = item.get('visual_extraction', {}).get('action', "")
#         window_pattern = r'window-id="\{([^}]*)\}"'
#         window_match = re.search(window_pattern, action)
#         guid = ""
#         if window_match:
#             guid = window_match.group(1)

#         # If no window-id, try to extract just the sheet id
#         # This assumes the sheet id is the last part of the action string
#         if not guid:
#             sheet_pattern = r'goto-sheet\s+(\S+)'
#             sheet_match = re.search(sheet_pattern, action)

#             if sheet_match:
#                 guid = sheet_match.group(1)

#         return [{
#             "properties": {
#                 "type": {
#                     "expr": {
#                         "Literal": {
#                             "Value": "'PageNavigation'"
#                         }
#                     }
#                 },
#                 "navigationSection": {
#                     "expr": {
#                         "Literal": {
#                             "Value": "'" + guid + "'"
#                         }
#                     }
#                 },
#                 "show": {
#                     "expr": {
#                         "Literal": {
#                             "Value": "true"
#                         }
#                     }
#                 }
#             }
#         }]

#     def generate_shape_background_section(self):
#         item = self.item
#         background_properties = get_nested_value(item, ['visual_container', 'border_padding', 'background_properties'], {})

#         if self.visual_type == "shape":
#             # Extract the background color from the container
#             container_color = background_properties.get('background_color', '#FFFFFF')

#             background_section = [
#                 {
#                     "properties": {
#                         "show": {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": "true"
#                                 }
#                             }
#                         },
#                         "color": {
#                             "solid": {
#                                 "color": {
#                                     "expr": {
#                                         "Literal": {
#                                             "Value": f"'{container_color}'"
#                                         }
#                                     }
#                                 }
#                             }
#                         },
#                         "transparency": {
#                             "expr": {
#                                 "Literal": {
#                                     "Value": "0D"
#                                 }
#                             }
#                         }
#                     }
#                 }
#             ]
#         else:
#             # For non-shape visuals, return None or use default background
#             background_section = None

#         return background_section

#     def generate_visualContainerFormattingObjects(self):
#         visualContainerFormattingObjects = VisualContainerFormattingObjects()
#         visualContainerFormattingObjects.title = self.generate_visual_title()

#         # Use shape background section for shape visuals, otherwise use regular background section
#         if self.visual_type == "shape":
#             background_section = self.generate_shape_background_section()
#         else:
#             background_section = self.generate_background_section()

#         if background_section:
#             visualContainerFormattingObjects.background = background_section
#         visualContainerFormattingObjects.border = self.generate_border_section()
#         visualContainerFormattingObjects.padding = self.generate_padding_section()
#         if self.visual_type == "actionButton" or (self.visual_type == 'image' and self.item.get('visual_extraction', {}).get('button_type') == 'image'):
#             visualContainerFormattingObjects.visualLink = self.generate_visual_link()
#         return visualContainerFormattingObjects


# # class BaseFilter:

# #     def generate_filter_objects(self):
# #         pass
