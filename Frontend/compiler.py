# frontend/compiler.py
import json
from pathlib import Path
from Frontend.transformer import PowerBIDashboardGenerator

class PBILayoutManager:
    """Calculates X, Y, Width, Height for Power BI visuals to avoid overlaps."""
    def __init__(self, canvas_width=1280, canvas_height=720):
        self.width = canvas_width
        self.height = canvas_height
        self.margin = 20
        self.current_y = 20

    def get_layout(self, visuals):
        kpis = [v for v in visuals if v.get('type') == 'card']
        charts = [v for v in visuals if v.get('type') != 'card']
        layout = []

        if kpis:
            card_w = (self.width - (len(kpis) + 1) * self.margin) // len(kpis)
            for i, kpi in enumerate(kpis):
                layout.append({**kpi, "x": self.margin + (i * (card_w + self.margin)), "y": self.current_y, "width": card_w, "height": 120})
            self.current_y += 140

        if charts:
            chart_w = (self.width - (3 * self.margin)) // 2
            for i, chart in enumerate(charts):
                row, col = divmod(i, 2)
                layout.append({**chart, "x": self.margin + (col * (chart_w + self.margin)), "y": self.current_y + (row * 320), "width": chart_w, "height": 300})
        return layout

def compile_to_pbip(project_name, frontend_spec):
    """
    Transforms Frontend JSON layout into the official Power BI PBIP .Report folder
    by invoking the PowerBIDashboardGenerator.
    """
    manager = PBILayoutManager()

    # 1. Calculate visual bounds using the layout manager
    positioned_visuals = manager.get_layout(frontend_spec.get('visuals', []))

    cells = []
    visuals_dict = {}

    # 2. Restructure frontend_spec into the format transformer.py expects
    for i, vis in enumerate(positioned_visuals):
        # Create a unique ID for each visual
        visual_id = vis.get('id', f"visual_{i}")

        # Append the cell layout data for the sheet
        cells.append({
            "name": visual_id,
            "type": vis.get('type', 'card'),
            "bounds": {
                "x": vis['x'],
                "y": vis['y'],
                "width": vis['width'],
                "height": vis['height']
            }
        })

        # Pass the visual definition to the visuals dictionary
        visuals_dict[visual_id] = vis

    # 3. Build the dashboard_meta_data dictionary
    dashboard_meta_data = {
        "sheets": {
            "Sheet1": {
                "qMeta": {"title": frontend_spec.get("title", "Dashboard")},
                "cells": cells,
                "rank": 1,
                "height": 100
            }
        },
        "visuals": visuals_dict,
        "dimensions": frontend_spec.get("dimensions", {}),
        "measures": frontend_spec.get("measures", {}),
        "master_objects": frontend_spec.get("master_objects", {})
    }

    # 4. Trigger the transformer's PBIP folder generation
    generator = PowerBIDashboardGenerator(project_name, dashboard_meta_data)
    generator.generate_complete_report()

    output_path = f"Data/Output/{project_name}/{project_name}.Report"
    print(f"Compilation complete. PBIP Report generated at: {output_path}")

    return output_path