from Frontend.Power_BI_Visuals.baseVisual import BaseVisual

class BaseElement(BaseVisual):
    def __init__(self, item) -> None:
        super().__init__(item)
        self.query_data_needed = False

    def generate_filter_object(self):
        return []