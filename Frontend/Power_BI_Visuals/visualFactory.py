from typing import Any, Type

# from Frontend.Power_BI_Visuals.StaticElements.textBox import TextBox
# from Frontend.Power_BI_Visuals.StaticElements.imageContainer import ImageContainer
from Frontend.Power_BI_Visuals.DynamicElements.table import PivotTable
from Frontend.Power_BI_Visuals.DynamicElements.barChart import BarChart
from Frontend.Power_BI_Visuals.DynamicElements.pieChart import PieChart
from Frontend.Power_BI_Visuals.DynamicElements.gauge import Gauge
from Frontend.Power_BI_Visuals.DynamicElements.lineChart import LineChart
from Frontend.Power_BI_Visuals.DynamicElements.heatMap import HeatMap
from Frontend.Power_BI_Visuals.DynamicElements.bubbleChart import BubbleChart
from Frontend.Power_BI_Visuals.DynamicElements.kpi import KPI
from Frontend.Power_BI_Visuals.DynamicElements.multiMetricKPI import MultiMetricKPI
from Frontend.Power_BI_Visuals.DynamicElements.comparisonKPI import ComparisonKPI
from Frontend.Power_BI_Visuals.baseVisual import BaseVisual


class VisualFactory:
    """Factory class to create PowerBI visual objects based on visualType"""

    _visual_map: dict[str, Type[BaseVisual]] = {
        'barchart': BarChart,
        'linechart': LineChart,
        'kpi': KPI,
        'gauge': Gauge,
        'treemap': HeatMap

    }

    @classmethod
    def create_visual(cls, visual_id, visual_type, visual_definition, visual_bounds, sheet_height) -> BaseVisual:
        visual_class = cls._visual_map.get(visual_type, None)
        # background_properties = get_nested_value(data, ['visual_container', 'border_padding', 'background_properties'], {})
        # if visual_type == 'shape' and background_properties.get('has_background') == False:
        #     print(f"Found shape visual with no background {visual_type}")
        #     return None

        # if not visual_class:
        #     print(f"Unsupported visual type: {visual_type}")
        #     return None

        dimension_mapping = {
            "product_category_name" : "Product_Category",
            "estimated_delivery" : "Dim_Orders",
            "Product_Category.product_category_name_english": "Product_Category",
            "Year" : "MasterCalendar",
            "customer_unique_id_dim" : "Dim_Customers",
            "Month" : "MasterCalendar",
            "seller_id" : "Dim_Sellers",
            "OrderDate" : "Dim_Orders",
            "FrequencySegment" : "Customers_RFM_Segmented",
            "rfm_monetary_segment" : "Dim_Customers"
        }

        visual = visual_class(visual_id, visual_type, visual_definition, visual_bounds, sheet_height, dimension_mapping)
        # visual.set_themes(themes)
        return visual
