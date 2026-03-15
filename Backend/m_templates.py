# Databricks M-Code Template (Navigation-based)
DATABRICKS_M_CODE_TEMPLATE = """
                let
                    Source = Databricks.Catalogs(Server, HTTPPath, [Catalog=null, Database=null]),
                    Database_Level = Source{{[Name=Database,Kind="Database"]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Redshift M-Code Template
REDSHIFT_M_CODE_TEMPLATE = """
                let
                    Source = AmazonRedshift.Database(Server, Database),
                    Schema_Level = Source{{[Name="{Schema}"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# CSV M-Code Template
CSV_M_CODE_TEMPLATE = """
                let
                    Source = Csv.Document(File.Contents(File_Path & "\{table_name}.csv"),[Delimiter=",", Columns=11, Encoding=1252, QuoteStyle=QuoteStyle.None]),
                    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
                in
                    #"Promoted Headers"
"""

# Excel M-Code Template
EXCEL_M_CODE_TEMPLATE = """
                let
                    Source = Excel.Workbook(File.Contents(File_Path & "\{table_name}.xlsx"), null, true),
                    Sheet1_Sheet = Source{{[Item="Sheet1",Kind="Sheet"]}}[Data],
                    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true])
                in
                    #"Promoted Headers"
"""

# SQL Server/ Azure SQL Database/ Azure Synapse Analytics M-Code Template
SQLSERVER_M_CODE_TEMPLATE = """
                let
                    Source = Sql.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Snowflake M-Code Template
SNOWFLAKE_M_CODE_TEMPLATE = """
                let
                    Source = Snowflake.Databases(Server, Warehouse),
                    Database_Level = Source{{[Name=Database,Kind="Database"]}}[Data],
                    Schema_Level = Database_Level{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Postgres M-Code Template
POSTGRESQL_M_CODE_TEMPLATE = """
                let
                    Source = PostgreSQL.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Oracle M-Code Template
ORACLE_M_CODE_TEMPLATE = """
                let
                    Source = Oracle.Database(Server, [HierarchicalNavigation=true]),
                    Schema_Level = Source{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Big Query M-Code Template
BIGQUERY_M_CODE_TEMPLATE = """
                let
                    Source = GoogleBigQuery.Database(),
                    Project_Level = Source{{[Name=Project,Kind="Project"]}}[Data],
                    Dataset_Level = Project_Level{{[Name="{Dataset}",Kind="Schema"]}}[Data],
                    Table_Level = Dataset_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# MySQL M-Code Template
MYSQL_M_CODE_TEMPLATE = """
                let
                    Source = MySQL.Database(Server, Database, [ReturnSingleDatabase=true]),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# SAP HANA M-Code Template
SAPHANA_M_CODE_TEMPLATE = """
                let
                    Source = SapHana.Database(Server, [Implementation="2.0"]),
                    Schema_Level = Source{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# IBM DB2 M-Code Template
DB2_M_CODE_TEMPLATE = """
                let
                    Source = Db2.Database(Server, Database),
                    Schema_Level = Source{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Teradata M-Code Template
TERADATA_M_CODE_TEMPLATE = """
                let
                    Source = Teradata.Database(Server, [Query=null]),
                    Schema_Level = Source{{[Name="{Schema}",Kind="Database"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Athena M-Code Template
ATHENA_M_CODE_TEMPLATE = """
                let
                    Source = AmazonAthena.Databases(),
                    Catalog_Level = Source{{[Id="AwsDataCatalog",Kind="Database"]}}[Data],
                    Schema_Level = Catalog_Level{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Maria DB M-Code Template
MARIADB_M_CODE_TEMPLATE = """
                let
                    Source = MariaDB.Contents(Server),
                    Database_Level = Source{{[Name="{Schema}",Kind="Database"]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Microsoft Dataverse M-Code Template
DATAVERSE_M_CODE_TEMPLATE = """
                let
                    Source = Cds.Databases(Server),
                    Table_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# SAP Business Warehouse M-Code Template
SAPBW_M_CODE_TEMPLATE = """
                let
                    Source = SapBw.Cubes(Server, SystemNumber, ClientId, [Implementation="2.0"]),
                    Catalog_Level = Source{{[Name="{Schema}",Kind="Catalog"]}}[Data],
                    Cube_Level = Catalog_Level{{[Name="{table_name}",Kind="Cube"]}}[Data]
                in
                    Cube_Level
"""

# OData Feed M-Code Template
ODATA_M_CODE_TEMPLATE = """
                let
                    Source = OData.Feed(Server, null, [Implementation="2.0"]),
                    Table_Level = Source{{[Name="{table_name}",Signature="table"]}}[Data]
                in
                    Table_Level
"""

# SharePoint M-Code Template
SHAREPOINT_LIST_M_CODE_TEMPLATE = """
                let
                    Source = SharePoint.Tables(Server, [ApiVersion = 15]),
                    Table_Level = Source{{[Id="{table_name}"]}}[Items]
                in
                    Table_Level
"""

# ODBC M-Code Template
ODBC_M_CODE_TEMPLATE = """
                let
                    Source = Odbc.DataSource(Server, [HierarchicalNavigation=true]),
                    Database_Level = Source{{[Name=Database,Kind="Database"]}}[Data],
                    Schema_Level = Database_Level{{[Name="{Schema}",Kind="Schema"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# Azure Table Storage M-Code Template
AZURE_TABLE_M_CODE_TEMPLATE = """
                let
                    Source = AzureStorage.Tables(Server),
                    Table_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Google Analytics M-Code Template
GOOGLE_ANALYTICS_M_CODE_TEMPLATE = """
                let
                    Source = GoogleAnalytics.Accounts(),
                    Account_Level = Source{{[Id="{AccountID}"]}}[Data],
                    Property_Level = Account_Level{{[Id="{PropertyID}"]}}[Data],
                    View_Level = Property_Level{{[Id="{ViewID}"]}}[Data],
                    Table_Level = View_Level{{[Id="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Salesforce Objects M-Code Template
SALESFORCE_M_CODE_TEMPLATE = """
                let
                    Source = Salesforce.Data(),
                    Table_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Adobe Analytics M-Code Template
ADOBE_ANALYTICS_M_CODE_TEMPLATE = """
                let
                    Source = AdobeAnalytics.Cubes(),
                    ReportSuite = Source{{[Id="{Schema}"]}}[Data],
                    Table_Level = ReportSuite{{[Id="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# IBM Informix M-Code Template
INFORMIX_M_CODE_TEMPLATE = """
                let
                    Source = Informix.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# MongoDB M-Code Template
MONGODB_M_CODE_TEMPLATE = """
                let
                    Source = MongoDB.Databases(Server, [Query=null]),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Azure Cosmos DB M-Code Template
COSMOS_DB_M_CODE_TEMPLATE = """
                let
                    Source = DocumentDB.Contents(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Sybase M-Code Template
SYBASE_M_CODE_TEMPLATE = """
                let
                    Source = Sybase.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Vertica M-Code Template
VERTICA_M_CODE_TEMPLATE = """
                let
                    Source = Vertica.Database(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Schema_Level = Database_Level{{[Name="{Schema}"]}}[Data],
                    Table_Level = Schema_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Web (JSON/REST API) M-Code Template
WEB_REST_M_CODE_TEMPLATE = """
                let
                    Source = Json.Document(Web.Contents(Server)),
                    Table_Level = Table.FromRecords(Source[result][{table_name}])
                in
                    Table_Level
"""

# Azure Data Lake Storage Gen2 M-Code Template
ADLS_GEN2_M_CODE_TEMPLATE = """
                let
                    Source = AzureStorage.DataLake(Server),
                    Files = Source{[Name="{Schema}"]}[Data],
                    Table_Level = Files{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Impala M-Code Template
IMPALA_M_CODE_TEMPLATE = """
                let
                    Source = Impala.Database(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# IBM Netezza M-Code Template
NETEZZA_M_CODE_TEMPLATE = """
                let
                    Source = Netezza.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Denodo M-Code Template
DENODO_M_CODE_TEMPLATE = """
                let
                    Source = Denodo.Contents(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Presto M-Code Template
PRESTO_M_CODE_TEMPLATE = """
                let
                    Source = Presto.Database(Server),
                    Catalog_Level = Source{{[Name="{Schema}"]}}[Data],
                    Table_Level = Catalog_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Apache Hive M-Code Template
HIVE_M_CODE_TEMPLATE = """
                let
                    Source = Hive.Database(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Google Sheets M-Code Template
GOOGLE_SHEETS_M_CODE_TEMPLATE = """
                let
                    Source = GoogleSheets.Contents(Server),
                    Spreadsheet = Source{{[name="{table_name}"]}}[Data]
                in
                    Spreadsheet
"""

# Microsoft Exchange Online M-Code Template
EXCHANGE_M_CODE_TEMPLATE = """
                let
                    Source = Exchange.Contents(Server),
                    Folder_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Folder_Level
"""

# Essbase M-Code Template
ESSBASE_M_CODE_TEMPLATE = """
                let
                    Source = Essbase.Cubes(Server),
                    Application = Source{{[Name="{Schema}"]}}[Data],
                    Cube_Level = Application{{[Name="{table_name}"]}}[Data]
                in
                    Cube_Level
"""

# Spark M-Code Template
SPARK_M_CODE_TEMPLATE = """
                let
                    Source = Spark.Databases(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Azure Data Explorer (Kusto) M-Code Template
KUSTO_M_CODE_TEMPLATE = """
                let
                    Source = AzureDataExplorer.Contents(Server, Database, "{table_name}", [])
                in
                    Source
"""

# Azure Blob Storage M-Code Template
AZURE_BLOB_M_CODE_TEMPLATE = """
                let
                    Source = AzureStorage.Blobs(Server),
                    Container = Source{{[Name="{Schema}"]}}[Data],
                    Table_Level = Container{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Azure Analysis Services (AAS) M-Code Template
AZURE_AS_M_CODE_TEMPLATE = """
                let
                    Source = AnalysisServices.Databases(Server),
                    Database_Level = Source{{[Name=Database]}}[Data],
                    Model_Level = Database_Level{{[Name="Model"]}}[Data],
                    Table_Level = Model_Level{{[Item="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# HDInsight Interactive Query (Hive) M-Code Template
HDINSIGHT_HIVE_M_CODE_TEMPLATE = """
                let
                    Source = HDInsight.Contents(Server),
                    Database_Level = Source{{[Name="{Schema}",Kind="Database"]}}[Data],
                    Table_Level = Database_Level{{[Name="{table_name}",Kind="Table"]}}[Data]
                in
                    Table_Level
"""

# PostgreSQL (Azure Managed) M-Code Template
AZURE_POSTGRES_M_CODE_TEMPLATE = """
                let
                    Source = AzurePostgreSQL.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# MySQL (Azure Managed) M-Code Template
AZURE_MYSQL_M_CODE_TEMPLATE = """
                let
                    Source = AzureMySQL.Database(Server, Database),
                    Table_Level = Source{{[Schema="{Schema}",Item="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Smartsheet M-Code Template
SMARTSHEET_M_CODE_TEMPLATE = """
                let
                    Source = Smartsheet.Tables(),
                    Table_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Zendesk M-Code Template
ZENDESK_M_CODE_TEMPLATE = """
                let
                    Source = Zendesk.Contents(Server),
                    Table_Level = Source{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# GitHub M-Code Template
GITHUB_M_CODE_TEMPLATE = """
                let
                    Source = GitHub.Contents(),
                    Repo = Source{{[Name="{Schema}"]}}[Data],
                    Table_Level = Repo{{[Name="{table_name}"]}}[Data]
                in
                    Table_Level
"""

# Microsoft Dataflows (Legacy/Standard) M-Code Template
DATAFLOW_M_CODE_TEMPLATE = """
                let
                    Source = PowerBI.Dataflows([]),
                    Workspace = Source{{[workspaceName="{Schema}"]}}[Data],
                    Dataflow = Workspace{{[dataflowName=Database]}}[Data],
                    Table_Level = Dataflow{{[entity="{table_name}"]}}[Data]
                in
                    Table_Level
"""
