from Frontend.Power_BI_Visuals.StaticElements.baseElement import BaseElement

from pathlib import Path

class ImageContainer(BaseElement):
    def __init__(self, item) -> None:
        super().__init__(item)

    # def generate_projections(self, axis_data):
    #     return {}

    def generate_visual_specific_properties(self):
        return {"image": self.generate_image_properties()}

    def generate_general_properties(self):
        item = self.item
        path = item.get('path', "")
        image_resource_name = Path(path).name

        return [{
            "properties": {
                "imageUrl": {
                    "expr": {
                        "ResourcePackageItem": {
                            "PackageName": "RegisteredResources",
                            "PackageType": 1,
                            "ItemName": image_resource_name
                        }
                    }
                },
                "scaling": {
                    "expr": {
                        "Literal": {
                            "Value": "'Fit'"
                        }
                    }
                }
            }
        }]

    def generate_image_properties(self):
        item = self.item
        path = item.get('path', "")
        image_resource_name = Path(path).name

        return [{
            "properties": {
                "sourceFile": {
                "image": {
                    "name": {
                    "expr": {
                        "Literal": {
                        "Value": f"'{image_resource_name}'"
                        }
                    }
                    },
                    "url": {
                    "expr": {
                        "ResourcePackageItem": {
                        "PackageName": "RegisteredResources",
                        "PackageType": 1,
                        "ItemName": image_resource_name
                        }
                    }
                    },
                    "scaling": {
                    "expr": {
                        "Literal": {
                        "Value": "'Normal'"
                        }
                    }
                    }
                }
                }
            }
        }]