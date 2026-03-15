import json
from pathlib import Path
import shutil
from typing import Any, Dict
import copy

from Frontend.Power_BI_Visuals.visualFactory import VisualFactory

import logging
logger = logging.getLogger(__name__)

class PowerBIDashboardGenerator:
    def __init__(self, project_name, frontend_spec):
        self.project_name = project_name
        self.report_title = frontend_spec.get("title", project_name)
        self.pages = frontend_spec.get("pages", [])

    def generate_complete_report(self):
        logger.info("Creating complete Power BI report structure...")
        try:
            self.output_folder = Path(f"Data/Output/{self.project_name}/{self.project_name}.Report")
            self.output_folder.mkdir(parents=True, exist_ok=True)

            self._create_pbi_folder()
            # self.registered_resources = self._create_static_resources()
            self._create_static_resources()
            self._create_definition_folder()
            self._create_platform_file()
            self._create_definition_file()

            logger.info(f"Complete PBI Report: {self.output_folder.absolute()}")
        except Exception:
            logger.exception("Failed to generate complete report")
            raise

    def _create_pbi_folder(self):
        pbi_folder = self.output_folder / ".pbi"
        try:
            pbi_folder.mkdir(parents=True, exist_ok=True)
            local_settings = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/localSettings/1.0.0/schema.json"
            }
            with open(pbi_folder / "localSettings.json", "w", encoding="utf-8") as f:
                json.dump(local_settings, f, indent=2)
            logger.info("Created .pbi/localSettings.json")
        except (PermissionError, OSError) as e:
            logger.error(f"Failed writing localSettings.json: {e}", exc_info=True)
            raise
    #Add Exception Handling
    def _create_definition_folder(self):
        """Generate complete folder structure"""
        definition_folder = self.output_folder / "definition"
        definition_folder.mkdir(exist_ok=True)

        self._create_report_json(definition_folder)
        self._create_version_json(definition_folder)

        pages_folder = self._create_pages_folder(definition_folder)

        for page in self.pages:
            page_id = page.get("id")
            page_name = page.get("name")
            display_name = page.get("displayName")
            visuals = page.get("visuals", [])
            visual_id = visual.get("id")
            visual_type = visual.get("type")

            visual_bounds = visual.get("bounds", {
                "x":0,
                "y":0,
                "width":300,
                "height":200
            })

            # Create page folder
            page_folder = self._create_page_folder(pages_folder, page_id)
            self._create_page_json(
                page_folder,
                page_id,
                page_name,
                display_name,
                visual_bounds.get("height", 200)
            )

            visuals_folder = self._create_visuals_folder(page_folder)

            for visual in visuals:

                visual_id = visual.get("id")
                visual_type = visual.get("type")

                visual_bounds = visual.get("bounds", {
                    "x":0,
                    "y":0,
                    "width":300,
                    "height":200
                })

                self._process_visual(
                    visuals_folder,
                    visual,
                )

            logger.info(f"{page_id} → {len(visuals)} visuals processed")

        self._create_pages_json(pages_folder)
        logger.info(f"Complete: {self.output_folder.absolute()}")

    def _create_static_resources(self):
        static_folder = self.output_folder / "StaticResources"
        try:
            static_folder.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            logger.error(f"Cannot create StaticResources folder: {e}", exc_info=True)
            raise

        # registered = self._create_register_resources(static_folder)
        self._create_shared_resources(static_folder)
        logger.info("Created StaticResources")
        # return registered

    def _create_platform_file(self):
        platform_file = self.output_folder / ".platform"
        platform_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {"type": "Report", "displayName": self.project_name},
            "config": {"version": "2.0", "logicalId": self.project_name},
        }
        try:
            with open(platform_file, "w", encoding="utf-8") as f:
                json.dump(platform_data, f, indent=2)
            logger.info("Created .platform")
        except Exception:
            logger.exception("Failed writing .platform")
            raise

    def _create_definition_file(self):
        definition_file = self.output_folder / "definition.pbir"
        definition_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
            "version": "4.0",
            "datasetReference": {"byPath": {"path": f"../{self.project_name}.SemanticModel"}},
        }
        try:
            with open(definition_file, "w", encoding="utf-8") as f:
                json.dump(definition_data, f, indent=2)
            logger.info("Created definition.pbir")
        except Exception:
            logger.exception("Failed writing definition.pbir")
            raise

    def _create_report_json(self, definition_folder):
        report_json = definition_folder / "report.json"
        report_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json",
        "themeCollection": {
            "baseTheme": {
            "name": "CY24SU10",
            "reportVersionAtImport": {
                "visual": "1.8.95",
                "report": "2.0.95",
                "page": "1.3.95"
            },
            "type": "SharedResources"
            }
        },
        "objects": {
            "section": [
            {
                "properties": {
                "verticalAlignment": {
                    "expr": {
                    "Literal": {
                        "Value": "'Top'"
                    }
                    }
                }
                }
            }
            ]
        },
        "resourcePackages": [
            {
            "name": "SharedResources",
            "type": "SharedResources",
            "items": [
                {
                "name": "CY24SU10",
                "path": "BaseThemes/CY24SU10.json",
                "type": "BaseTheme"
                }
            ]
            }
        ],
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": "AllowSummarized",
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True
        }
        }
        try:
            with open(report_json, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2)
            logger.info("Created report.json")
        except Exception:
            logger.exception("Failed writing report.json")
            raise

    def _create_version_json(self, definition_folder: Path):
        version_json = definition_folder / "version.json"
        version_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
            "version": "2.0.0"
        }
        try:
            with open(version_json, "w", encoding="utf-8") as f:
                json.dump(version_data, f, indent=2)
            logger.info(f"Created version.json")
        except Exception as e:
            logger.error(f"Failed writing version.json")

    def _create_pages_folder(self, definition_folder: Path) -> Path:
        pages_folder = definition_folder / "pages"
        try:
            pages_folder.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.exception("Failed creating pages folder")
            raise
        return pages_folder

    def _create_page_folder(self, pages_folder: Path, page_id: str) -> Path:
        page_folder = pages_folder / page_id
        try:
            page_folder.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.exception(f"Failed creating folder for {page_id}")
            raise
        return page_folder

    def _create_page_json(self, page_folder, page_id, page_name, display_name, height):
        BASE_WIDTH = 1280
        BASE_HEIGHT = 720
        calculated_height = (float(height) / 100.0) * BASE_HEIGHT
        page_json = page_folder / "page.json"
        page_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
            "name": page_id,
            "displayName": display_name,
            "displayOption": "FitToPage",
            "height": calculated_height,
            "width": BASE_WIDTH
        }
        try:
            with open(page_json, "w", encoding="utf-8") as f:
                json.dump(page_data, f, indent=2)
            logger.info(f"Created page.json at {page_folder}")
        except Exception as e:
            logger.error(f"Failed writing page.json at {page_folder}")

    def _create_visuals_folder(self, page_folder: Path) -> Path:
        visuals_folder = page_folder / "visuals"
        try:
            visuals_folder.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.exception("Failed creating visuals folder")
            raise
        return visuals_folder

    def _process_visual(self, visuals_folder, visual):
        """Uses existing VisualFactory"""
        visual_id = visual.get("id")
        visual_type = visual.get("type")

        if not visual_id or not visual_type:
            raise ValueError("Visual must contain id and type")
            
        visual_bounds = visual.get(
            "bounds",
            {
                "x": 0,
                "y": 0,
                "width": 300,
                "height": 200
            }
        )
        table = visual.get("table")
        dimensions = visual.get("dimensions", [])
        measures = visual.get("measures", [])
        filters = visual.get("filters", [])
        properties = visual.get("properties", {})
        visual_folder = visuals_folder / visual_id
        try:
            visual_folder.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.exception(f"Failed creating visual folder for visual with id: {visual_id}")
            raise

        try:
            visual_definition = {
                "table": table,
                "dimensions": dimensions,
                "measures": measures,
                "filters": filters,
                "properties": properties
            }
            visual_factory = VisualFactory()
            visual_obj = visual_factory.create_visual(
                visual_id = visual_id,
                visual_type = visual_type,
                definition = visual_definition,
                bounds = visual_bounds
            )
            pbi_visual = visual_obj.generate_visual()

            clean_dict = pbi_visual.model_dump(
                    mode='json',           # JSON-compatible output
                    by_alias = True,       # Use aliases in output
                    exclude_none=True      # Skip None/unset fields
                    )
            (visual_folder / "visual.json").write_text(json.dumps(clean_dict, indent=2))

        except Exception as e:
            (visual_folder / "visual.json").write_text(json.dumps({
                "metadata": {"visualID": visual_id},
                "error": str(e)
            }, indent=2))

    def _create_pages_json(self, pages_folder: Path):
        """
        Create pages.json with page order and active page based on sheet rank.

        Args:
            pages_folder: Path object to folder where pages.json will be saved
        """
        try:
            # Ensure folder exists
            pages_folder.mkdir(parents=True, exist_ok=True)

            if not self.pages:
                logger.warning("No pages provided")
                page_ids = []
                active_page_id = ""
            else:
                # List of all sheet IDs
                page_ids = [page["id"] for page in self.pages]

                # Warn if rank missing
                for sheet_id, layout in self.sheets.items():
                    if "rank" not in layout:
                        logger.warning(
                            f"Sheet '{sheet_id}' missing 'rank'; assuming infinity for sorting"
                        )

                # Find sheet with lowest rank
                active_page_id = page_ids[0] if page_ids else ""

            pages_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
                "pageOrder": page_ids,
                "activePageName": active_page_id
            }

            try:
                pages_file = pages_folder / "pages.json"
                with open(pages_file, "w", encoding="utf-8") as f:
                    json.dump(pages_json, f, indent=2)
                logger.info(f"Created {pages_file}")
            except Exception as e:
                logger.error(f"Failed to write to {pages_file}: {e}")

            logger.info(
                f"pages.json created successfully at '{pages_file}' "
                f"with active page '{active_page_id}'"
            )

        except Exception as e:
            logger.error(f"Failed to create pages.json : {e}", exc_info = True)

    def _create_shared_resources(self, static_folder: Path):
        shared_folder = static_folder / "SharedResources"
        try:
            shared_folder.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            logger.error(f"Cannot create SharedResources folder: {e}", exc_info=True)
            raise

        CY24SU10_data: Dict[str, Any] = {}
        CY24SU10_path = Path(__file__).parent / "CY24SU10.json"
        if CY24SU10_path.is_file():
            try:
                with open(CY24SU10_path, "r", encoding="utf-8") as f:
                    CY24SU10_data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse CY24SU10.json: {e}", exc_info=True)
            except Exception:
                logger.exception("Error reading CY24SU10.json")

        try:
            with open(shared_folder / "CY24SU10.json", "w", encoding="utf-8") as f:
                json.dump(CY24SU10_data, f, indent=2)
            logger.info("Created shared CY24SU10.json")
        except Exception:
            logger.exception("Failed writing shared CY24SU10.json")
            raise

# Update it later only used when images are used
    def _create_register_resources(self, static_folder):
        """Copy all images from assets/{dossierId}/ FLAT to RegisterResources/ (unique names)"""
        register_folder = static_folder / "RegisterResources"
        register_folder.mkdir(exist_ok=True)

        # Direct path to assets/{dossierId}/
        assets_dossier_folder = Path("./assets") / self.dossier_id

        if not assets_dossier_folder.exists():
            print(f"Assets folder not found: {assets_dossier_folder}")
            return

        print(f"Found assets folder: {assets_dossier_folder}")

        copied_files: list[str] = []

        # Copy ALL files FLAT - NO CONFLICT HANDLING NEEDED (unique names)
        for file_path in assets_dossier_folder.rglob('*'):
            if file_path.is_file():
                dest_path = register_folder / file_path.name  # ✅ Direct copy

                shutil.copy2(file_path, dest_path)
                print(f"   📄 {file_path.name} → {dest_path.name}")
                copied_files.append(file_path.name)

        print(f"Copied {len(copied_files)} images FLAT to RegisterResources/")
        return copied_files


def transformation(project_name,dashboard_meta_data: Dict[str, Dict[str, Any]]):
    # CREATE OBJECT & PASS JSON PATH
    generator = PowerBIDashboardGenerator(project_name, dashboard_meta_data)

    # CALL MAIN FUNCTION (creates everything)
    generator.generate_complete_report()