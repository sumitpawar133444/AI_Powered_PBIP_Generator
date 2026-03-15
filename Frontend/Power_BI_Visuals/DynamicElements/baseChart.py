import uuid
import re
from Frontend.Power_BI_Visuals.baseVisual import BaseVisual


class BaseChart(BaseVisual):

    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds)

    def generate_chart_properties(self):
        return {}


    def generate_filter_object(self) -> list:
        """
        Generate Power BI filter field bindings for dimensions and measures.
        Handles:
            - Dimensions → Categorical filters
            - Library measures → Measure binding
            - Inline measures → Aggregation binding
        """

        filters = []

        dimensions = self.data.get("qDimensions", [])
        measures = self.data.get("qMeasures", [])
        for dim in dimensions:
            table = self.data.get("qMeasures", [])

            filters.append({
                "name": uuid.uuid4().hex[:20],
                "field": {
                    "Column": {
                        "Expression": {
                            "SourceRef": {
                                "Entity": table
                            }
                        },
                        "Property": dim
                    }
                },
                "type": "Categorical"
            })

        for measure in measures:
                filters.append({
                    "name": uuid.uuid4().hex[:20],
                    "field": {
                        "Measure": {
                            "Expression": {
                                "SourceRef": {
                                    "Entity": "measure"
                                }
                            },
                            "Property": measure_name
                        }
                    },
                    "type": "Advanced"
                })
        
        return filters