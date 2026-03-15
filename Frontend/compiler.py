# frontend/compiler.py
import json
import logging
import sys
from pathlib import Path
from Frontend.transformer import PowerBIDashboardGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def compile_to_pbip(project_name, frontend_spec):
    """
    Transforms Frontend JSON layout into the official Power BI PBIP .Report folder
    by invoking the PowerBIDashboardGenerator.
    """

    logger.info(f"Generating report: {project_name}")

    # 4. Trigger the transformer's PBIP folder generation
    generator = PowerBIDashboardGenerator(project_name, frontend_spec)
    generator.generate_complete_report()

    output_path = f"Data/Output/{project_name}/{project_name}.Report"
    print(f"Compilation complete. PBIP Report generated at: {output_path}")

    return output_path