from typing import Any, Type
from Frontend.Power_BI_Visuals.DynamicElements.table import PivotTable
from Frontend.Power_BI_Visuals.DynamicElements.barChart import BarChart
from Frontend.Power_BI_Visuals.DynamicElements.pieChart import PieChart
from Frontend.Power_BI_Visuals.DynamicElements.gauge import Gauge
from Frontend.Power_BI_Visuals.DynamicElements.lineChart import LineChart
from Frontend.Power_BI_Visuals.DynamicElements.heatMap import HeatMap
from Frontend.Power_BI_Visuals.DynamicElements.bubbleChart import BubbleChart
from Frontend.Power_BI_Visuals.DynamicElements.kpi import KPI
from Frontend.Power_BI_Visuals.DynamicElements.card import Card
from Frontend.Power_BI_Visuals.DynamicElements.multiMetricKPI import MultiMetricKPI
from Frontend.Power_BI_Visuals.DynamicElements.comparisonKPI import ComparisonKPI
from Frontend.Power_BI_Visuals.baseVisual import BaseVisual


class VisualFactory:
    """Factory class to create PowerBI visual objects based on visualType"""

    _visual_map: dict[str, Type[BaseVisual]] = {
        'bar': BarChart,
        'line': LineChart,
        'pie': PieChart,
        'table': PivotTable,
        'card': Card,
        'kpi': KPI,
        'gauge': Gauge,
        'treemap': HeatMap

    }

    @classmethod
    def create_visual(cls, visual_id, visual_type, visual_definition, visual_bounds) -> BaseVisual:
        visual_class = cls._visual_map.get(visual_type, None)
        if not visual_class:
            raise ValueError(f"Unsupported visual type: {visual_type}")
        visual = visual_class(visual_id, visual_type, visual_definition, visual_bounds)
        # visual.set_themes(themes)
        return visual
