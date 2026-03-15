# from Power_BI_Visuals.StaticElements.baseElement import BaseElement
# from utils.general_utils import rgb_to_hex, px_to_pt, extract_first_font_family

# class TextBox(BaseElement):
#     def __init__(self, item) -> None:
#         super().__init__(item)


#     def generate_visual_specific_properties(self):
#         item = self.item
#         text_content = item.get('text', None)
#         styles = item.get('styles', {})
#         powerbi_text_style = {}

#         font_size_raw = styles.get('fontSize')
#         font_size_pt = px_to_pt(font_size_raw)
#         if font_size_pt:
#             powerbi_text_style['fontSize'] = font_size_pt

#         font_family_raw = styles.get('fontFamily')
#         powerbi_text_style['fontFamily'] = extract_first_font_family(font_family_raw)

#         font_color_raw = styles.get('color')
#         if font_color_raw:
#             powerbi_text_style['color'] = rgb_to_hex(font_color_raw)

#         font_weight = styles.get('fontWeight')
#         if font_weight and int(font_weight) > 500:
#             powerbi_text_style['fontWeight'] = 'bold'

#         paragraph = {
#             "textRuns": [{
#                 "value": text_content,
#                 "textStyle": powerbi_text_style
#             }]
#         }

#         return {"general": [{"properties": {"paragraphs": [paragraph]}}]}