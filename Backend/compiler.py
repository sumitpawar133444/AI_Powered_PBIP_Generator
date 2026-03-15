# backend/compiler.py
import os
import json
import shutil
import re, uuid, base64
import streamlit as st
from typing import List, Dict, Tuple
from Core.utils import GuidRegistry
from Backend.m_templates import *

PBIP_TEMPLATE = {
    "version": "1.0",
    "artifacts": [{"report": {"path": "<app name>.Report"}}],
    "settings": {"enableAutoRecovery": True}
}

PBISM_TEMPLATE = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "4.2",
    "settings": {}
}

GITIGNORE_CONTENT = """**/.pbi/localSettings.json
**/.pbi/cache.abf
"""

EDITOR_SETTINGS_TEMPLATE = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/editorSettings/1.0.0/schema.json",
    "showHiddenFields": True,
    "autodetectRelationships": True,
    "parallelQueryLoading": True,
    "typeDetectionEnabled": True,
    "relationshipImportEnabled": True,
    "runBackgroundAnalysis": True,
    "shouldNotifyUserOfNameConflictResolution": True
}

LOCAL_SETTINGS_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/localSettings/1.1.0/schema.json"

EN_US_TMDL_CONTENT = """cultureInfo en-US

    linguisticMetadata =
            {
              "Version": "1.0.0",
              "Language": "en-US"
            }
        contentType: json
"""

def _generate_security_bindings_signature() -> str:
    random_bytes = os.urandom(32)
    return base64.b64encode(random_bytes).decode("ascii")

def generate_database_tmdl() -> str:
    return "database\n  compatibilityLevel: 1567"

def generate_expressions_tmdl(backend_spec: Dict) -> str:
    tmdl_lines = []
    added_params = set()

    for table_spec in backend_spec.get('tables', []):
        conn = table_spec.get("connection", {})
        source_type = conn.get("sourceType", "csv").lower()
        server_value = conn.get("server")
        database_value = conn.get("database")

        if server_value and "Server" not in added_params:
            tmdl_lines.append(f'expression Server = "{server_value}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')
            tmdl_lines.append(f'    lineageTag: {uuid.uuid4()}')
            tmdl_lines.append(f'    annotation PBI_ResultType = Text\n')
            added_params.add("Server")

        if database_value and "Database" not in added_params:
            tmdl_lines.append(f'expression Database = "{database_value}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')
            tmdl_lines.append(f'    lineageTag: {uuid.uuid4()}')
            tmdl_lines.append(f'    annotation PBI_ResultType = Text\n')
            added_params.add("Database")

        # Add Source-Specific Parameters
        if source_type == "databricks":
            # 4. Extract directly from connection instead of undefined qlik_config
            http_path_value = conn.get("httpPath")
            if http_path_value and "HTTP_Path" not in added_params:
                tmdl_lines.append(f'expression HTTP_Path = "{http_path_value}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')
                tmdl_lines.append(f'    lineageTag: {uuid.uuid4()}')
                tmdl_lines.append(f'    annotation PBI_ResultType = Text\n')
                added_params.add("HTTP_Path")

        elif source_type in ["csv", "excel"]:
            file_path_value = conn.get("filePath", "C:\\Data")
            if file_path_value and "File_Path" not in added_params:
                tmdl_lines.append(f'expression File_Path = "{file_path_value}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')
                tmdl_lines.append(f'    lineageTag: {uuid.uuid4()}')
                tmdl_lines.append(f'    annotation PBI_ResultType = Text\n')
                added_params.add("File_Path")

    return "\n".join(tmdl_lines)

def write_definition_pbism(semantic_dir: str) -> str:
    os.makedirs(semantic_dir, exist_ok=True)
    dest_path = os.path.join(semantic_dir, "definition.pbism")
    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(PBISM_TEMPLATE, f, indent=2)
    return dest_path

def write_platform_file(display_name: str, semantic_dir: str) -> str:
    os.makedirs(semantic_dir, exist_ok=True)
    dest_path = os.path.join(semantic_dir, ".platform")

    platform_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {
            "type": "SemanticModel",
            "displayName": display_name
        },
        "config": {
            "version": "2.0",
            "logicalId": str(uuid.uuid4())
        }
    }

    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(platform_content, f, indent=2)

    return dest_path

def write_definition_pbism(semantic_dir: str) -> str:
    os.makedirs(semantic_dir, exist_ok=True)
    dest_path = os.path.join(semantic_dir, "definition.pbism")
    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(PBISM_TEMPLATE, f, indent=2)
    return dest_path

def write_pbi_files(semantic_dir: str) -> dict:
    pbi_dir = os.path.join(semantic_dir, ".pbi")
    os.makedirs(pbi_dir, exist_ok=True)

    editor_path = os.path.join(pbi_dir, "editorSettings.json")
    with open(editor_path, "w", encoding="utf-8") as f:
        json.dump(EDITOR_SETTINGS_TEMPLATE, f, indent=2)

    local_settings = {
        "$schema": LOCAL_SETTINGS_SCHEMA,
        "userConsent": {},
        "securityBindingsSignature": _generate_security_bindings_signature()
    }
    local_path = os.path.join(pbi_dir, "localSettings.json")
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(local_settings, f, indent=2)

    return {
        "editorSettings": editor_path,
        "localSettings": local_path
    }

def write_en_us_culture_file(semantic_dir: str) -> str:
    definition_dir = os.path.join(semantic_dir, "definition")
    cultures_dir = os.path.join(definition_dir, "cultures")
    os.makedirs(cultures_dir, exist_ok=True)
    dest_path = os.path.join(cultures_dir, "en-US.tmdl")

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(EN_US_TMDL_CONTENT)
    return dest_path

def write_pbip_file(display_name: str, project_dir: str) -> str:
    dest_path = os.path.join(project_dir, f"{display_name}.pbip")
    content = PBIP_TEMPLATE.copy()
    content["artifacts"][0]["report"]["path"] = f"{display_name}.Report"

    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    return dest_path

def write_gitignore_file(project_dir: str) -> str:
    dest_path = os.path.join(project_dir, ".gitignore")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT)
    return dest_path

def write_database_file(definition_dir):
    content = generate_database_tmdl()
    path = os.path.join(definition_dir, "database.tmdl")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def write_expressions_file(semantic_dir, backend_spec):
    try:
        content = generate_expressions_tmdl(backend_spec)
        if not content.strip():
            return
        definition_dir = os.path.join(semantic_dir, "definition")
        os.makedirs(definition_dir, exist_ok=True)
        output_path = os.path.join(definition_dir, "expression.tmdl")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        st.error(f"Failed to generate expressions.tmdl: {str(e)}")
        print(f"Failed to generate expressions.tmdl: {str(e)}")

def get_m_code_for_table(table_name, connection):
    """
    Generates dynamic M code based on connection details from the JSON spec.
    """
    source_type = connection.get("sourceType", "Excel").lower()
    schema_name = connection.get("schema").lower()
    dataset_name = connection.get("dataset").lower()
    account_id = connection.get("account_id").lower()
    property_id = connection.get("property_id").lower()
    view_id = connection.get("view_id").lower()

    if source_type == "databricks":
        return DATABRICKS_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "redshift":
        return REDSHIFT_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "sqlserver":
        return SQLSERVER_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "snowflake":
        return SNOWFLAKE_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "postgresql":
        return POSTGRESQL_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "oracle":
        return ORACLE_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "bigquery":
        return BIGQUERY_M_CODE_TEMPLATE.format(table_name=table_name, Dataset = dataset_name)
    elif source_type == "mysql":
        return MYSQL_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "saphana":
        return SAPHANA_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "db2":
        return DB2_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "teradata":
        return TERADATA_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "athena":
        return ATHENA_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "mariadb":
        return MARIADB_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "dataverse":
        return DATAVERSE_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "sapbw":
        return SAPBW_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "odata":
        return ODATA_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "sharepoint list":
        return SHAREPOINT_LIST_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "odbc":
        return ODBC_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "azure table":
        return AZURE_TABLE_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "google analytics":
        return GOOGLE_ANALYTICS_M_CODE_TEMPLATE.format(table_name=table_name, AccountID = account_id, PropertyID = property_id, ViewID = view_id)
    elif source_type == "salesforce":
        return SALESFORCE_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "adobe analytics":
        return ADOBE_ANALYTICS_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "informix":
        return INFORMIX_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "mongodb":
        return MONGODB_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "cosmosdb":
        return COSMOS_DB_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "sybase":
        return SYBASE_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "vertica":
        return VERTICA_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "web":
        return WEB_REST_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "adls gen2":
        return ADLS_GEN2_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "impala":
        return IMPALA_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "netezza":
        return NETEZZA_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "denodo":
        return DENODO_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "presto":
        return PRESTO_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "hive":
        return HIVE_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "google sheets":
        return GOOGLE_SHEETS_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "exchange":
        return EXCHANGE_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "essbase":
        return ESSBASE_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "spark":
        return SPARK_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "kusto":
        return KUSTO_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "azure blob storage":
        return AZURE_BLOB_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "azure analysis service":
        return AZURE_AS_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "hdinsight":
        return HDINSIGHT_HIVE_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "azure postgresql":
        return AZURE_POSTGRES_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "azure mysql":
        return AZURE_MYSQL_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "smartsheet":
        return SMARTSHEET_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "zendesk":
        return ZENDESK_M_CODE_TEMPLATE.format(table_name=table_name)
    elif source_type == "github":
        return GITHUB_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "dataflow":
        return DATAFLOW_M_CODE_TEMPLATE.format(table_name=table_name, Schema = schema_name)
    elif source_type == "excel":
        return EXCEL_M_CODE_TEMPLATE.format(table_name=table_name)
    else:
        return CSV_M_CODE_TEMPLATE.format(table_name=table_name)

def generate_table_tmdl(table_spec, registry):
    """
    Generates the TMDL definition for a single table, including columns,
    measures, and connection-based M code.
    """
    t_name = table_spec["name"]
    cols = table_spec.get("columns", [])
    connection = table_spec.get("connection", {})

    # Generate Column TMDL
    cols_tmdl = []
    for c in cols:
        c_name = c["name"]
        dtype = c.get("dataType", "string")
        col_block = f"""
    column '{c_name}'
        dataType: {dtype}
        lineageTag: {registry.get_new_guid()}
        sourceColumn: '{c_name}'
"""
        if dtype == "dateTime":
            g = registry.register_date_column(t_name, c_name)
            col_block += f"""
        variation Variation
            isDefault
            relationship: {g['relationship_guid']}
            defaultHierarchy: '{g['local_table_name']}'.'Date Hierarchy'
"""
            col_block += "\n        annotation SummarizationSetBy = Automatic\n"
        cols_tmdl.append(col_block)

    # Get Dynamic M Code
    m_code = get_m_code_for_table(t_name, connection)

    # Combine into Table TMDL
    tmdl = f"""
table '{t_name}'
    lineageTag: {registry.get_new_guid()}
{''.join(cols_tmdl)}
    partition '{t_name}' = m
        mode: import
        source = {m_code}

    annotation PBI_ResultType = Table
    annotation PBI_NavigationStepName = Navigation
"""
    return tmdl

def generate_hidden_date_template(guid_registry: GuidRegistry) -> Tuple[str, str]:
    """Generates the standard hidden DateTableTemplate required by Power BI."""
    table_guid = guid_registry.get_new_guid()
    name = f"DateTableTemplate_{table_guid}"
    tmdl = f"""
table '{name}'
    isHidden
    isPrivate
    lineageTag: {guid_registry.get_new_guid()}

    column Date
        dataType: dateTime
        isHidden
        formatString: General Date
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: PaddedDateTableDates
        summarizeBy: none
        isNameInferred
        sourceColumn: [Date]
        annotation SummarizationSetBy = User

    column Year = YEAR([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: Years
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = Year

    column MonthNo = MONTH([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: MonthOfYear
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = MonthNumber

    column Month = FORMAT([Date], "MMMM")
        dataType: string
        isHidden
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: Months
        summarizeBy: none
        sortByColumn: MonthNo
        annotation SummarizationSetBy = User
        annotation TemplateId = Month

    column QuarterNo = INT(([MonthNo] + 2) / 3)
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: QuarterOfYear
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = QuarterNumber

    column Quarter = "Qtr " & [QuarterNo]
        dataType: string
        isHidden
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: Quarters
        summarizeBy: none
        sortByColumn: QuarterNo
        annotation SummarizationSetBy = User
        annotation TemplateId = Quarter

    column Day = DAY([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {guid_registry.get_new_guid()}
        dataCategory: DayOfMonth
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = Day

    hierarchy 'Date Hierarchy'
        lineageTag: {guid_registry.get_new_guid()}

        level Year
            lineageTag: {guid_registry.get_new_guid()}
            column: Year

        level Quarter
            lineageTag: {guid_registry.get_new_guid()}
            column: Quarter

        level Month
            lineageTag: {guid_registry.get_new_guid()}
            column: Month

        level Day
            lineageTag: {guid_registry.get_new_guid()}
            column: Day

        annotation TemplateId = DateHierarchy

    partition '{name}' = calculated
        mode: import
        source = Calendar(Date(2015,1,1), Date(2015,1,1))

    annotation __PBI_TemplateDateTable = true
    annotation DefaultItem = 'Date Hierarchy'
"""
    return name, tmdl

def generate_local_date_table(main_table: str, source_column: str, guid_info: Dict) -> str:
    """Generates a LocalDateTable for a specific date variation."""
    name = guid_info['local_table_name']
    tmdl = f"""
table '{name}'
    isHidden
    showAsVariationsOnly
    lineageTag: {guid_info['local_table_guid']}

    column Date
        dataType: dateTime
        isHidden
        formatString: General Date
        lineageTag: {uuid.uuid4()}
        dataCategory: PaddedDateTableDates
        summarizeBy: none
        isNameInferred
        sourceColumn: [Date]
        annotation SummarizationSetBy = User

    column Year = YEAR([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {uuid.uuid4()}
        dataCategory: Years
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = Year

    column MonthNo = MONTH([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {uuid.uuid4()}
        dataCategory: MonthOfYear
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = MonthNumber

    column Month = FORMAT([Date], "MMMM")
        dataType: string
        isHidden
        lineageTag: {uuid.uuid4()}
        dataCategory: Months
        summarizeBy: none
        sortByColumn: MonthNo
        annotation SummarizationSetBy = User
        annotation TemplateId = Month

    column QuarterNo = INT(([MonthNo] + 2) / 3)
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {uuid.uuid4()}
        dataCategory: QuarterOfYear
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = QuarterNumber

    column Quarter = "Qtr " & [QuarterNo]
        dataType: string
        isHidden
        lineageTag: {uuid.uuid4()}
        dataCategory: Quarters
        summarizeBy: none
        sortByColumn: QuarterNo
        annotation SummarizationSetBy = User
        annotation TemplateId = Quarter

    column Day = DAY([Date])
        dataType: int64
        isHidden
        formatString: 0
        lineageTag: {uuid.uuid4()}
        dataCategory: DayOfMonth
        summarizeBy: none
        annotation SummarizationSetBy = User
        annotation TemplateId = Day

    hierarchy 'Date Hierarchy'
        lineageTag: {uuid.uuid4()}

        level Year
            lineageTag: {uuid.uuid4()}
            column: Year

        level Quarter
            lineageTag: {uuid.uuid4()}
            column: Quarter

        level Month
            lineageTag: {uuid.uuid4()}
            column: Month

        level Day
            lineageTag: {uuid.uuid4()}
            column: Day

        annotation TemplateId = DateHierarchy

    partition '{name}' = calculated
        mode: import
        source = Calendar(Date(Year(MIN('{main_table}'[{source_column}])), 1, 1), Date(Year(MAX('{main_table}'[{source_column}])), 12, 31))

    annotation __PBI_LocalDateTable = true
"""
    return tmdl

def generate_measures_table_tmdl(measures_list, registry):
    """
    Generates a dedicated dummy table containing all root-level measures.
    """
    measure_blocks = []

    for item in measures_list:
        name = item.get("name", "Unnamed Measure")
        formula = item.get("formula", "BLANK()")

        # Sanitize name to prevent TMDL syntax errors
        safe_name = name.replace("'", "''")

        measure_blocks.append(
            f"\n    measure '{safe_name}' = {formula}\n"
            f"        lineageTag: {registry.get_new_guid()}\n"
        )

    indent_4 = " " * 4
    indent_8 = " " * 8

    # Create the table definition with the dummy placeholder column
    tmdl = f"""table 'measure'
{indent_4}lineageTag: {registry.get_new_guid()}
{"".join(measure_blocks)}
{indent_4}column 'Measure Placeholder'
{indent_8}dataType: string
{indent_8}isHidden
{indent_8}lineageTag: {registry.get_new_guid()}
{indent_8}summarizeBy: none
{indent_8}sourceColumn: [Column1]

{indent_4}partition 'measure-part' = m
{indent_8}mode: import
{indent_8}source =
{indent_8}    let
{indent_8}        Source = Table.FromRows({{}}, type table [Column1 = any])
{indent_8}    in
{indent_8}        Source

{indent_4}annotation PBI_Id = {uuid.uuid4().hex}
"""
    return tmdl

def build_pbip_semantic_model(backend_spec: Dict, project_name: str):
    """Generates the full TMDL folder structure for the semantic model."""
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    output_base = os.path.join(PROJECT_ROOT, "Data", "Output", project_name)
    semantic_dir = os.path.join(output_base, f"{project_name}.semantic-model")
    definition_dir = os.path.join(semantic_dir, "definition")
    tables_dir = os.path.join(definition_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(os.path.join(semantic_dir, ".pbi"), exist_ok=True)

    registry = GuidRegistry()
    processed_tables = []

    write_platform_file(project_name, semantic_dir)
    write_definition_pbism(semantic_dir)
    write_pbi_files(semantic_dir)
    write_en_us_culture_file(semantic_dir)
    write_pbip_file(project_name, output_base)
    write_gitignore_file(output_base)
    write_database_file(definition_dir)
    write_expressions_file(semantic_dir, backend_spec)

    for table_spec in backend_spec.get('tables', []):
        t_name = table_spec.get('name', 'Table1')
        tmdl_content = generate_table_tmdl(table_spec, registry)

        with open(os.path.join(tables_dir, f"{t_name}.tmdl"), "w", encoding="utf-8") as f:
            f.write(tmdl_content)
        processed_tables.append(t_name)

    # 2. NEW: Generate the Dedicated Measures Table
    measures_list = backend_spec.get("measures", [])
    if measures_list:
        measures_tmdl = generate_measures_table_tmdl(measures_list, registry)

        # Save it as _Measures.tmdl (using underscore forces it to the top of the field pane in PBI)
        with open(os.path.join(tables_dir, "_Measures.tmdl"), "w", encoding="utf-8") as f:
            f.write(measures_tmdl)
        processed_tables.append("_Measures")

    # 3. Generate Local Date Tables (one for each date column found)
    for (t_name, c_name), info in registry.date_variations.items():
        local_tmdl = generate_local_date_table(t_name, c_name, info)
        with open(os.path.join(tables_dir, f"{info['local_table_name']}.tmdl"), "w", encoding="utf-8") as f:
            f.write(local_tmdl)

    # 4. Generate the hidden DateTableTemplate
    tpl_name, tpl_tmdl = generate_hidden_date_template(registry)
    with open(os.path.join(tables_dir, f"{tpl_name}.tmdl"), "w", encoding="utf-8") as f:
        f.write(tpl_tmdl)

    # 5. Generate relationships.tmdl (including Date behavior)
    rel_lines = []
    for (t_name, c_name), info in registry.date_variations.items():
        rel = f"relationship {info['relationship_guid']}\n    joinOnDateBehavior: datePartOnly\n    fromColumn: '{t_name}'.'{c_name}'\n    toColumn: '{info['local_table_name']}'.Date\n"
        rel_lines.append(rel)

    # Add any explicit data relationships from the backend_spec
    for rel_data in backend_spec.get('relationships', []):
        rel = f"relationship {uuid.uuid4()}\n    fromColumn: '{rel_data['fromTable']}'.'{rel_data['fromColumn']}'\n    toColumn: '{rel_data['toTable']}'.'{rel_data['toColumn']}'\n"
        rel_lines.append(rel)

    with open(os.path.join(definition_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(rel_lines))

    processed_tables.sort()
    ref_lines = []
    for t in processed_tables:
        if ' ' in t or not re.match(r"^[a-zA-Z0-9_]+$", t):
            ref_lines.append(f"ref table '{t}'")
        else:
            ref_lines.append(f"ref table {t}")

    model_content = f"""
model Model
    culture: en-US
    defaultPowerBIDataSourceVersion: powerBI_V3
    sourceQueryCulture: en-US
    dataAccessOptions
        legacyRedirects
        returnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBI_QueryOrder = {json.dumps(processed_tables)}

annotation PBI_ProTooling = ["DevMode"]

{chr(10).join(ref_lines)}

ref cultureInfo en-US
"""
    with open(os.path.join(definition_dir, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(model_content)
    print(" Generated model.tmdl")

    print(f" Migration complete for {project_name}")

def bundle_pbip_to_zip(project_path, zip_name):
    shutil.make_archive(zip_name, 'zip', project_path)
    return f"{zip_name}.zip"