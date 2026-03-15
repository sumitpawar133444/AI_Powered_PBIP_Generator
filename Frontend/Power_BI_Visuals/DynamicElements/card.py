from Frontend.Power_BI_Visuals.DynamicElements.baseChart import BaseChart

class Card(BaseChart):
    def __init__(self, item) -> None:
        super().__init__(item)

    def generate_visual_query(self):
        dataset = self.item.get('dataSet', 'DataSet')  # Fallback to 'DataSet' if not found

        return {
            "queryState": {
                "Data": {
                "projections": [
                    {
                    "field": {
                        "Aggregation": {
                        "Expression": {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Entity": dataset
                                }
                            },
                            "Property": "Revenue"
                            }
                        },
                        "Function": 0
                        }
                    },
                    "queryRef": f"Sum({dataset}.Revenue)",
                    "nativeQueryRef": "Sum of Revenue"
                    }
                ]
                }
            },
            "sortDefinition": {
                "sort": [
                {
                    "field": {
                    "Aggregation": {
                        "Expression": {
                        "Column": {
                            "Expression": {
                            "SourceRef": {
                                "Entity": dataset
                            }
                            },
                            "Property": "Revenue"
                        }
                        },
                        "Function": 0
                    }
                    },
                    "direction": "Descending"
                }
                ],
                "isDefaultSort": True
            }
        }

    def generate_filter_object(self):
        dataset = self.item.get('dataSet', 'DataSet')  # Fallback to 'DataSet' if not found

        return [
            {
                "name": "col_filter_0",
                "field": {
                "Aggregation": {
                    "Expression": {
                    "Column": {
                        "Expression": {
                        "SourceRef": {
                            "Entity": dataset
                        }
                        },
                        "Property": "Revenue"
                    }
                    },
                    "Function": 0
                }
                },
                "type": "Advanced"
            }
        ]

    def generate_visual_specific_properties(self):
        return {}