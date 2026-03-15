import uuid
import re
from Frontend.Power_BI_Visuals.baseVisual import BaseVisual


class BaseChart(BaseVisual):

    def __init__(self, visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping) -> None:
        super().__init__(visual_id, visual_type, visual_defintion, visual_bounds, sheet_height, dimension_mapping)

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

        hypercube = self.data.get("qHyperCubeDef", {})
        dimensions = hypercube.get("qDimensions", [])
        measures = hypercube.get("qMeasures", [])

        for dim in dimensions:
            field_name = (
                dim.get("definition", {})
                .get("qDef", {})
                .get("qFieldDefs", [None])[0]
            )

            if not field_name:
                continue

            table = self.dimension_mp.get(field_name)

            filters.append({
                "name": uuid.uuid4().hex[:20],
                "field": {
                    "Column": {
                        "Expression": {
                            "SourceRef": {
                                "Entity": table
                            }
                        },
                        "Property": field_name
                    }
                },
                "type": "Categorical"
            })


        for measure in measures:

            definition = measure.get("definition", {})
            measure_name = definition.get("qLabel", "")

            # 🔥 Detect library measure
            is_library = measure.get("source") == "library"

            # ---------------------------------------------
            # CASE A: LIBRARY MEASURE → Use Measure binding
            # ---------------------------------------------
            if is_library:
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

            # ---------------------------------------------
            # CASE B: INLINE MEASURE → Parse aggregation
            # ---------------------------------------------
            else:
                agg_name, column_name = self._parse_qlik_measure(measure_name)

                func_code = self._get_agg_function_code(agg_name)

                filters.append({
                    "name": uuid.uuid4().hex[:20],
                    "field": {
                        "Aggregation": {
                            "Expression": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Entity": "table"
                                        }
                                    },
                                    "Property": column_name
                                }
                            },
                            "Function": func_code
                        }
                    },
                    "type": "Advanced"
                })

        return filters


    # =========================================================
    # 🔧 Helper: Parse Qlik Measure Expression
    # =========================================================

    def _parse_qlik_measure(self, expression: str):
        """
        Parse Qlik expression like:
            Sum(Sales)
            Avg(Revenue)
            Count(Distinct CustomerID)

        Returns:
            agg_name (PascalCase)
            column_name
        """

        match = re.match(r'(\w+)\((.*?)\)', expression.strip(), re.IGNORECASE)

        if not match:
            return "Sum", expression  # fallback

        agg = match.group(1)
        column = match.group(2)

        # Clean distinct if present
        column = column.replace("Distinct", "").strip()

        # Convert to PascalCase
        agg = agg[0].upper() + agg[1:].lower()

        return agg, column


    # =========================================================
    # 🔢 Helper: Aggregation → Function Code
    # =========================================================

    def _get_agg_function_code(self, agg: str) -> int:
        """
        Map exact PascalCase aggregation names
        to Power BI Function numeric codes.
        """

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

        return agg_function_map.get(agg, 0)