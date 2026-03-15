from __future__ import annotations
from pydantic import BaseModel, RootModel, Field
from typing import Any, Literal
from enum import Enum

class ArithmeticOperatorKind(RootModel):
    root: Literal[0, 1, 2, 3]


class Axis(BaseModel):

    Groups: list['AxisGroup'] = Field(
        ..., description='Ordered list of hierarchical groupings in this axis.'
    )
    Name: str = Field(
        ..., description='Name by which the axis is referenced in the query.'
    )



class AxisGroup(BaseModel):

    Keys: list['QueryExpressionContainer'] = Field(
        ..., description='List of expressions that define the keys of this group.'
    )
    Subtotal: bool


class EntitySource(BaseModel):
    
    Name: str = Field(
        ..., description='Name by which the table is referenced in the query'
    )
    Entity: str | None = Field(
        None, description='Reference name of the table in the data.'
    )
    Schema: str | None = Field(
        None,
        description='Identifier for the schema which contains the entity source.  This can be omitted if the Schema name is the default.',
    )
    Expression: 'QueryExpressionContainer | None' = Field(
        None,
        description='An expression that produces a table. Mandatory if Type is Expression.',
    )
    Type: 'EntitySourceType | None' = Field(
        0, description='Type of entity source - defaults to Table (0)'
    )


class EntitySourceType(RootModel):
    root: Literal[0, 1, 2]


class FilterDefinition(BaseModel):
    
    Version: float | None = Field(2,
        # const=True,
        description='Version of the query'
    )
    From: list[EntitySource] = Field(
        ..., description='Set of tables from which the data will be picked.'
    )
    Where: list['QueryFilter'] = Field(
        ..., description='Set of filters to apply to the data.'
    )


class IncludeAllTypes(RootModel):
    root: Literal[0, 1, 2]


class QueryAggregationExpression(BaseModel):

    Function: 'QueryAggregateFunction' = Field(
        ..., description='Type of the aggregation.'
    )
    Expression: 'QueryExpressionContainer' = Field(
        ..., description='Expression to aggregate.'
    )
    

class QueryAggregateFunction(RootModel):
    root: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]


class QueryAllRolesRefExpression(BaseModel):
    pass


class QueryAnyValueExpression(BaseModel):

    DefaultValueOverridesAncestors: bool | None = Field(
        None,
        description='When true, any interaction with the a model-specified default value override results in all attribute relationship path ancestors being overridden.',
    )


class QueryArithmeticExpression(BaseModel):

    Left: 'QueryExpressionContainer' = Field(..., description='First operand expression')
    Right: 'QueryExpressionContainer' = Field(
        ..., description='Second operand expression'
    )
    Operator: ArithmeticOperatorKind = Field(
        ..., description='The arithmetic operation to perform'
    )


class QueryBetweenExpression(BaseModel):
    
    Expression: 'QueryExpressionContainer' = Field(
        ..., description='Expression to compare.'
    )
    LowerBound: 'QueryExpressionContainer' = Field(
        ..., description='Lower (inclusive) bound for the value of the expression.'
    )
    UpperBound: 'QueryExpressionContainer' = Field(
        ..., description='Upper (inclusive) bound for the value of the expression.'
    )


class QueryBinaryExpression(BaseModel):

    root: 'QueryStartsWithExpression | None'


class QueryCase(BaseModel):
    
    Condition: 'QueryExpressionContainer' = Field(
        ...,
        description='An expression producing a boolean indicating whether or not to match this Case.',
    )
    Value: 'QueryExpressionContainer' = Field(
        ..., description='An expression producing the result when this case is matched.'
    )


class QueryComparisonExpression(BaseModel):
    
    ComparisonKind: 'QueryComparisonKind' = Field(
        ..., description='Type of the comparison.'
    )
    Left: 'QueryExpressionContainer' = Field(
        ..., description='First expression to which to apply the operator.'
    )
    Right: 'QueryExpressionContainer' = Field(
        ..., description='Second expression to which to apply the operator.'
    )


class QueryConditionalExpression(BaseModel):
    
    Cases: list[QueryCase] = Field(
        ...,
        description='Cases are considered in the specified order.\nThe result is the Case.Value of the first case where Case.Condition evaluates to true.\nIf no Case.Condition evaluates to true, the result is the DefaultValue, if DefaultValue is specified.\nOtherwise, the result is null.',
    )
    DefaultValue: 'QueryExpressionContainer | None' = Field(
        None, description='An optional value to return when no case evaluates to true.'
    )


class QueryColumnExpression(BaseModel):
    root: 'QueryMeasureExpression | None'


class QueryComparisonKind(RootModel):
    root: Literal[0, 1, 2, 3, 4]


class QueryContainsExpression(BaseModel):
    root: 'QueryStartsWithExpression | None'


class QueryDateAddExpression(BaseModel):
    
    Amount: float = Field(..., description='Number of units to add to the date.')
    Time_Unit: 'TimeUnit' = Field(..., description='Unit of time to add to the date.', alias="TimeUnit")
    Expression: 'QueryExpressionContainer' = Field(
        ..., description='Expression to which to add.'
    )


class QueryDateSpanExpression(BaseModel):

    Time_Unit: 'TimeUnit' = Field(
        ..., description='Unit of time used for datespan function.', alias="TimeUnit"
    )
    Expression: 'QueryExpressionContainer' = Field(
        ..., description='Expression to which to apply the datespan function.'
    )


class QueryDefaultValueExpression(BaseModel):
    pass


class QueryDefinition(BaseModel):
    
    Version: float | None = Field(2,
        # const=True,
        description='Version of the query'
    )
    From: list[EntitySource] = Field(
        ..., description='Set of tables from which the data will be picked.'
    )
    Where: list['QueryFilter'] | None = Field(
        None, description='Set of filters to apply to the data.'
    )
    OrderBy: list['QuerySortClause'] | None = Field(
        None, description='List of expressions over which to sort the results.'
    )
    Select: list['QueryExpressionContainer'] = Field(
        ..., description='List of expressions to display in the results.'
    )
    VisualShape: list[Axis] | None = Field(
        None,
        description='Provides metadata information about the structure and state of the visualization.',
    )
    GroupBy: list['QueryExpressionContainer'] | None = Field(
        None,
        description="List of expressions that represent the items to group by.\nThese additional groupings can be columns that we don't project or entity tables.",
    )
    Transform: list['QueryTransform'] | None = Field(
        None,
        description='List of table manipulation operations to apply within the query.',
    )
    Top: float | None = Field(
        None,
        description='When specified, the query will return up to the specified number of rows based on the specified OrderBy.',
    )


class QueryDiscretizeExpression(BaseModel):
    
    Expression: 'QueryExpressionContainer' = Field(
        ..., description='The expression to be discretized.'
    )
    Count: float = Field(
        ...,
        description='The number of discrete values to result from the transformation.',
    )


class QueryExistsExpression(BaseModel):
    
    Expression: 'QueryExpressionContainer' = Field(
        ...,
        description='Expression to verify there exists at least one instance of. Must be a SourceRef expression.',
    )


class QueryExpressionContainer(RootModel):

    root: 'QueryExpressionContainer1' = Field(
        ...,
        description='Holds a single expression and associated metadata.\nName, NativeReferenceName, and Annotations may be specified for any expression.\nEach other property represents a specific type of expression and exactly one of these other properties must be specified.',
    )


class QueryExpressionContainer1(BaseModel):
    
    Name: str | None = Field(
        None, description='The name by which the expression can be referenced'
    )
    NativeReferenceName: str | None = Field(
        None,
        description='The name by which the expression can be referenced in native expressions.',
    )
    Annotations: dict[str, Any] | None = Field(
        None, description='Auxiliary metadata for this expression.'
    )
    SourceRef: 'StandaloneSourceRefExpression | QuerySourceRefExpression | None' = Field(
        None,
        description='The SourceRef element contains an expression which is reference to a source table in the query or the data.',
    )
    Column: QueryColumnExpression | None = Field(
        None,
        description='The Column element contains an expression which is a reference to a column in a source table.',
    )
    Measure: 'QueryMeasureExpression | None' = Field(
        None,
        description='The Measure element contains an expression which is a reference to a measure in a source table.',
    )
    Min: 'QueryMinExpression | None' = Field(
        None,
        description='The Min element contains an expression whose min aggregation needs to be computed.',
    )
    Max: 'QueryMaxExpression | None' = Field(
        None,
        description='The Max element contains an expression whose max aggregation needs to be computed.',
    )
    Aggregation: QueryAggregationExpression | None = Field(
        None,
        description='The Aggregation element contains an expression which is an aggregation of an expression.',
    )
    Percentile: 'QueryPercentileExpression | None' = Field(
        None,
        description='The Percentile element contains an expression which computes a percentile of an expression.',
    )
    Hierarchy: 'QueryHierarchyExpression | None' = Field(
        None,
        description='Hierarchy is an element which represents a reference to a hierarchy in a source table.',
    )
    HierarchyLevel: 'QueryHierarchyLevelExpression | None' = Field(
        None,
        description='HierarchyLevel is an element which represents a reference to a hierarchy level in a hierarchy.',
    )
    PropertyVariationSource: 'QueryPropertyVariationSourceExpression | None' = Field(
        None,
        description='PropertyVariationSource is an element which represents a reference to a source of variations associated with a property.',
    )
    Subquery: 'QuerySubqueryExpression | None' = Field(
        None, description='Subquery is an element which holds a query.'
    )
    Discretize: QueryDiscretizeExpression | None = Field(
        None,
        description='Transforms a continuous space of numerical values into a discrete space of numerical values.',
    )
    And: QueryBinaryExpression | None = Field(
        None,
        description='The And element contains an expression which represents an "and" between two expressions that evaluate to a boolean value.',
    )
    Between: QueryBetweenExpression | None = Field(
        None,
        description='The Between element contains an expression which is a comparison between an expression and two bounds.',
    )
    In: 'QueryInExpression | None' = Field(
        None,
        description='The In element contains an expression which is a comparison between an ordered list of expressions and a set of ordered lists of values.\nIf the tuple defined in Expressions matches any tuple defined in Values, then In returns true.',
    )
    Or: QueryBinaryExpression | None = Field(
        None,
        description='The And element contains an expression which represents an "or" between two expressions that evaluate to a boolean value.',
    )
    Comparison: QueryComparisonExpression | None = Field(
        None,
        description='The Comparison element contains an expression which is a comparison between two expressions.',
    )
    Not: 'QueryNotExpression | None' = Field(
        None,
        description='The Not element contains an expression which represents a "not" of an expression that evaluate to a boolean value.',
    )
    Contains: QueryContainsExpression | None = Field(
        None,
        description='The Contains element contains an expression which is a "contains" comparison between two expressions.\nThe operation is case insensitive and accent sensitive.',
    )
    StartsWith: 'QueryStartsWithExpression | None' = Field(
        None,
        description='The StartsWith element contains an expression which is a "starts with" comparison between two expressions.',
    )
    Exists: QueryExistsExpression | None = Field(
        None,
        description='The Exists element contains an expression which represents confirming the existence of at least one instance of an expression.',
    )
    Literal: 'QueryLiteralExpression | None' = Field(
        None,
        description='The Literal element contains an expression which is a literal value.',
    )
    DateSpan: QueryDateSpanExpression | None = Field(
        None,
        description='The DateSpan element contains an expression which is a datespan calculation of an expression.\nA DateSpan can be compared directly to a Date via Comparison or Between.',
    )
    DateAdd: QueryDateAddExpression | None = Field(
        None,
        description='The DateAdd element contains an expression which is a dateadd calculation of an expression.',
    )
    Now: 'QueryNowExpression | None' = Field(
        None,
        description='The Now element contains an expression which returns the current date and time.',
    )
    DefaultValue: QueryDefaultValueExpression | None = Field(
        None,
        description='The DefaultValue element represents the model-defined default value for a column.\nIt may only be used as the Right expression in a Comparison expression with a ComparisonKind of Equal.',
    )
    AnyValue: QueryAnyValueExpression | None = Field(
        None,
        description='The AnyValue element represents a wildcard value that will match any value in a column.\nIt may only be used as the Right expression in a Comparison expression with a ComparisonKind of Equal.',
    )
    Arithmetic: QueryArithmeticExpression | None = Field(
        None,
        description='The Arithmetic element contains an expression which is an arithmetic operation on two expressions.',
    )
    Floor: 'QueryFloorExpression | None' = Field(
        None,
        description='The Floor element represents an operation to round the specified expression toward zero to a multiple of the specified size.',
    )
    ScopedEval: 'QueryScopedEvalExpression | None' = Field(
        None,
        description='ScopedEval is an element which evaluates an expression in a specified scope.',
    )
    FilteredEval: 'QueryFilteredEvalExpression | None' = Field(
        None,
        description='The FilteredEval element contains a set of filters to apply to the measure.',
    )
    TransformTableRef: 'QueryTransformTableRefExpression | None' = Field(
        None,
        description='The TransformTableRef element contains an expression which is reference to a TransformTable in the query.',
    )
    TransformOutputRoleRef: 'QueryTransformOutputRoleRefExpression | None' = Field(
        None,
        description='The TransformOutputRoleRef element contains an expression which is reference to a column produced by a Transform algorithm.\nThe reference is resolved by the Role attached to the output column by the transform.',
    )
    SparklineData: 'QuerySparklineDataExpression | None' = Field(
        None,
        description='Used to represent the data behind a sparkline. The data returned will be JSON formatted X/Y value pairs.',
    )
    NativeVisualCalculation: 'QueryNativeVisualCalc | None' = Field(
        None,
        description='The NativeVisualCalculation element represents invocation of an expression defined using an expression in an underlying query language.\nThe expression should be invoked in the Visual Calculation Context for this query.',
    )
    FillRule: 'QueryFillRuleExpression | None' = Field(
        None,
        description='The FillRule element represents an operation to apply a dynamic fill operation.',
    )
    GroupRef: 'QueryGroupRefExpression | None' = Field(
        None,
        description='The GroupRef element contains an expression which is a reference to a model grouping column.',
    )
    ResourcePackageItem: 'QueryResourcePackageItem | None' = Field(
        None,
        description='The ResourcePackageItem element contains an expression which references a ResourcePackage item.',
    )
    RoleRef: 'QueryRoleRefExpression | None' = Field(
        None,
        description='The RoleRef element contains an expression which is a reference to a named Role defined by a Visual.',
    )
    SummaryValueRef: 'QuerySummaryValueRefExpression | None' = Field(
        None,
        description='The SumaryValueRef element contains an expression which is a reference to a summary value in Insights Summary.',
    )
    AllRolesRef: QueryAllRolesRefExpression | None = Field(
        None,
        description='The AllRolesRef element is used to reference all the roles in a visual.',
    )
    SelectRef: 'QuerySelectRefExpression | None' = Field(
        None,
        description='The SelectRef element contains an expression which is a reference to a named item in the select clause of the query.',
    )
    ThemeDataColor: 'QueryThemeDataColorExpression | None' = Field(
        None,
        description='The ThemeDataColor element represents an operation to select a color from a theme.',
    )
    Conditional: QueryConditionalExpression | None = Field(
        None,
        description='The Conditional element represents an operation to select between several possible cases or an optional default.',
    )
    NativeMeasure: 'QueryNativeMeasure | None' = Field(
        None,
        description='The NativeMeasure element represents invocation of a measure defined using an expression in an underlying query language.',
    )
    NativeColumn: 'QueryNativeColumn | None' = Field(
        None,
        description='The NativeColumn element represents invocation of a column defined using an expression in an underlying query language.',
    )
    VisualTopN: 'QueryVisualTopNExpression | None' = Field(
        None,
        description='The VisualTopN element represents a type of filter that limits the amount of data points returned in a query',
    )


class QueryExpressionContentCache(BaseModel):
    
    Dependencies: list[QueryExpressionContainer] | None = None
    UnrecognizedIdentifiers: bool | None = None


class QueryFillRuleExpression(BaseModel):

    Input: QueryExpressionContainer = Field(
        ..., description='The expression providing the input value to the rule.'
    )
    FillRule: Any = Field(
        ...,
        description='Describes the algorithm, and associated parameters, needed to convert the Input into the desired fill.',
    )


class QueryFilter(BaseModel):
    
    Target: list[QueryExpressionContainer] | None = Field(
        None,
        description='Set of expressions over which the condition applies. Applied to the set of all non-aggregate, non-measure expressions in the Select if not specified.',
    )
    Condition: QueryExpressionContainer = Field(
        ...,
        description='Condition to apply to the target. Must be an expression that evaluates to a boolean.',
    )
    Annotations: dict[str, Any] | None = Field(
        None, description='Auxillary metadata for this filter.'
    )


class QueryFilteredEvalExpression(BaseModel):
    
    Expression: QueryExpressionContainer = Field(
        ...,
        description='The expression over which the condition applies. Must be a scalar.',
    )
    Filters: list[QueryFilter] = Field(
        ..., description='List of filters to apply to the measure.'
    )


class QueryFloorExpression(BaseModel):
    
    Expression: QueryExpressionContainer = Field(..., description='Expression to round')
    Size: float = Field(
        ...,
        description='Describes the desired multiple for rounding.\n- TimeUnit is specified: the expression is rounded to a Size multiples of the specified TimeUnit.\n- TimeUnit is omitted: the expression is rounded to a multiple of Size.',
    )
    Time_Unit: 'TimeUnit | None' = Field(
        None, description='The desired unit of rounding for Date/Time values.', alias="TimeUnit"
    )


class QueryGroupRefExpression(BaseModel):
    
    GroupedColumns: list[QueryExpressionContainer] = Field(
        ..., description='The underlying columns for the desired grouping.'
    )
    Expression: QueryExpressionContainer = Field(
        ...,
        description='Reference to the source table containing the property. Must be a SourceRef, PropertyVariationSource, or TransformTableRef expression.',
    )
    Property: str = Field(
        ..., description='The name of the target property in the source.'
    )


class QueryHierarchyExpression(BaseModel):        

    Expression: QueryExpressionContainer = Field(
        ...,
        description='Reference to the source table containing the hierarchy. Must be a SourceRef or a PropertyVariationSource expression.',
    )
    Hierarchy: str = Field(
        ..., description='The name of the target hierarchy in the source.'
    )


class QueryHierarchyLevelExpression(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ...,
        description='Reference to the hierarchy containing the level. Must be a Hierarchy expression.',
    )
    Level: str = Field(
        ..., description='The name of the target level in the hierarchy.'
    )


class QueryInExpression(BaseModel):        

    Expressions: list[QueryExpressionContainer] = Field(
        ..., description='The tuple of expressions to compare.'
    )
    Values: list[list[QueryExpressionContainer]] | None = Field(
        None, description='The tuples of values to compare with the expressions.'
    )
    Table: QueryExpressionContainer | None = Field(
        None,
        description='An expression, which must be a SourceRef, holding a table to compare against the Expressions.\nThe number of columns in the table must match the number of Expressions.\nEach row in the table is considered a tuple to be matched against the expressions.',
    )


class QueryLiteralExpression(BaseModel):
    
    Value: str = Field(
        ...,
        description='The value of the literal.\n- Boolean: "true"\n- DateTime: "datetime\'YYYY-MM-DDThh:mm:ss.ffffff"\n- Decimal: "2.4M"\n- Double: "2.4D"\n- Integer: "24L"\n- Number: ""\n- Null: "null"\n- String: "some string value"',
    )


class QueryMaxExpression(BaseModel):
    
    Include_All_Types: IncludeAllTypes = Field(
        ..., description='Defines how variant types should be treated.', alias="IncludeAllTypes"
    )
    Expression: QueryExpressionContainer = Field(
        ..., description='Expression whose min will be computed.'
    )


class QueryMeasureExpression(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ...,
        description='Reference to the source table containing the property. Must be a SourceRef, PropertyVariationSource, or TransformTableRef expression.',
    )
    Property: str = Field(
        ..., description='The name of the target property in the source.'
    )


class QueryMinExpression(QueryMaxExpression):
    pass


class QueryNativeColumn(BaseModel):
    
    DataType: float = Field(
        ..., description='The expected result data type of the native expression.'
    )
    Expression: str = Field(..., description='The expression to evaluate.')
    Language: str = Field(
        ...,
        description='The name of the underlying query language used to define Expression.',
    )
    Source: QueryExpressionContainer = Field(
        ...,
        description='Defines the table that this column should be considered as part of.',
    )
    ExpressionContentCache: QueryExpressionContentCache | None = Field(
        None, description='Holds metadata about the expression content.'
    )
    ProposedName: str | None = Field(
        None,
        description='The preferred name that should be used if the expression needs to be associated with a name in order to be evaluated.',
    )
    Format: str | None = Field(
        None,
        description='The format string that should be applied to the result of evaluating the expression.',
    )


class QueryNativeMeasure(BaseModel):

    DataType: float = Field(
        ..., description='The expected result data type of the native expression.'
    )
    Expression: str = Field(..., description='The expression to evaluate.')
    Language: str = Field(
        'dax',
        # const=True,
        description='The name of the underlying query language used to define Expression.',
    )
    ExpressionContentCache: QueryExpressionContentCache | None = Field(
        None, description='Holds metadata about the expression content.'
    )
    ProposedName: str | None = Field(
        None,
        description='The preferred name that should be used if the expression needs to be associated with a name in order to be evaluated.',
    )
    Format: str | None = Field(
        None,
        description='The format string that should be applied to the result of evaluating the expression.',
    )


class QueryNativeVisualCalc(BaseModel):

    Language: str = Field(
        'dax',
        # const=True,
        description='The name of the underlying query language that is used to define Expression (i.e., "Dax").',
    )
    Expression: str = Field(..., description='The expression to be evaluated.')
    Name: str = Field(..., description='The name of the calculation')
    DataType: 'QueryNativeVisualCalcDataType | None' = Field(
        None, description='The data type of visual calculation', alias="DataType"
    )


class QueryNativeVisualCalcDataType(Enum):
    Binary = 'Binary'
    Boolean = 'Boolean'
    Date = 'Date'
    DateTime = 'DateTime'
    DateTimeZone = 'DateTimeZone'
    Decimal = 'Decimal'
    Double = 'Double'
    Duration = 'Duration'
    Integer = 'Integer'
    Json = 'Json'
    None_ = 'None'
    Null = 'Null'
    Text = 'Text'
    Time = 'Time'
    Variant = 'Variant'


class QueryNotExpression(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ...,
        description='Expression to negate. Must be an expression that evaluates to a boolean value.',
    )


class QueryNowExpression(BaseModel):
    pass


class QueryPercentileExpression(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ..., description='The expression to be evaluated for the percentile.'
    )
    K: float = Field(
        ...,
        description='The desired percentile value.\n- Exclusive is true: K must be between 0 and 1, exclusive.\n- Exclusive is false: K must be between 0 and 1, inclusive.',
    )
    Exclusive: bool | None = Field(
        False,
        description='Indicates whether an inclusive or exclusive percentile should be computed.',
    )


class QueryPropertyVariationSourceExpression(BaseModel):
    
    Expression: QueryExpressionContainer = Field(
        ...,
        description='Reference to the source property containing the property variation source. Must be a SourceRef expression.',
    )
    Name: str = Field(
        ..., description='The name of the target variation source in the property.'
    )
    Property: str = Field(
        ..., description='The name of the target property in the SourceRef.'
    )


class QueryResourcePackageItem(BaseModel):
    
    PackageName: str = Field(..., description='Identifies the ResourcePackage.')
    PackageType: float = Field(
        ..., description='Identifies the type of resource package.'
    )
    ItemName: str = Field(
        ..., description='Identifies the item within the resource package'
    )


class QueryRoleRefExpression(BaseModel):
    
    Role: str = Field(..., description='The Name of the desired Role within a Visual.')


class QueryScopedEvalExpression(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ..., description='Expression to evaluate in the new scope.'
    )
    Scope: list[QueryExpressionContainer] = Field(
        ...,
        description='Set of expressions defining the new scope.  These expressions can only be Columns.',
    )


class QuerySelectRefExpression(BaseModel):
    
    ExpressionName: str = Field(
        ...,
        description='The Name of the ExpressionContainer from Select of the QueryDefinition.',
    )


class QuerySortClause(BaseModel):

    Expression: QueryExpressionContainer = Field(
        ..., description='Expression over which to sort the results.'
    )
    Direction: 'SortDirection' = Field(..., description='Indicates the direction to sort.')


class QuerySourceRefExpression(BaseModel):        

    Source: str = Field(..., description='Name of the source table in a query.')


class QuerySparklineDataExpression(BaseModel):
    
    Measure: QueryExpressionContainer = Field(
        ..., description='The measure to compute sparkline data for.'
    )
    Groupings: list[QueryExpressionContainer] = Field(
        ..., description='The granularity at which to evaluate the measure.'
    )
    PointsPerSparkline: float | None = Field(
        52,
        # const=True,
        description='Number of points per sparkline'
    )
    ApplyCalculationGroupTo: Literal["Sparkline", "Point"] | None = Field(
        None,
        description= "The granularity of the sparkline measure in the calculation group evaluation. This determines whether the\ncalculation group should apply to the entire sparkline or to each value of the sparkline. Defaults to entire\nsparkline (\"Sparkline\")"
    )


class QueryStartsWithExpression(BaseModel): 

    Left: QueryExpressionContainer = Field(
        ..., description='First expression to which to apply the operator.'
    )
    Right: QueryExpressionContainer = Field(
        ..., description='Second expression to which to apply the operator.'
    )


class QuerySubqueryExpression(BaseModel):
    
    Query: QueryDefinition = Field(..., description='The query to evaluate.')


class QuerySummaryValueRefExpression(BaseModel):

    Name: str = Field(
        ..., description='The Name of the summary value within a summary template.'
    )


class QueryThemeDataColorExpression(BaseModel):
    
    ColorId: float = Field(..., description='The theme color to select.')
    Percent: float


class QueryTransform(BaseModel):

    Name: str = Field(
        ...,
        description='The name used to refer to this transform in other parts of the query.\nThis name must be unique across all other Transform.Name values in this query.',
    )
    Algorithm: str = Field(..., description='The algorithm to apply.')
    Input: 'QueryTransformInput' = Field(
        ..., description='Describes the information needed to invoke the transform.'
    )
    Output: 'QueryTransformOutput' = Field(
        ..., description='Describes the expected results from the invoked transform.'
    )


class QueryTransformInput(BaseModel):

    Parameters: list[QueryExpressionContainer] = Field(
        ..., description='Parameters to be supplied when invoking the algorithm'
    )
    Table: 'QueryTransformTable | None' = Field(
        None, description='The structure of the table of data passed to the transform.'
    )


class QueryTransformOutput(BaseModel):
    
    Table: 'QueryTransformTable | None' = Field(
        None, description='The structure of the data produced by the transform.'
    )


class QueryTransformOutputRoleRefExpression(BaseModel):
    
    Role: str = Field(..., description='The Role of the target column.')
    Transform: str | None = Field(
        None,
        description='The Name of the target Transform. This must be omitted when used to define a column in the output table of a Transform.'
    )


class QueryTransformTable(BaseModel):
    
    Name: str = Field(
        ...,
        description='Name by which the transform is referenced in the query.\nThis name must be unique across all other TransformTable.Name values in the query.',
    )
    Columns: list['QueryTransformTableColumn'] = Field(
        ..., description='The columns that make up this table.'
    )


class QueryTransformTableColumn(BaseModel):
    
    Role: str | None = Field(
        None,
        description='An arbitrary string used to identify this column to the transform algorithm.  Role may not be unique.',
    )
    Expression: QueryExpressionContainer = Field(
        ...,
        description='The expression defining this column. ExpressionContainer.Name property defines the name of the column.\nExpressionContainer.Name is required and must be unique across all other columns in this table.',
    )


class QueryTransformTableRefExpression(BaseModel):

    Source: str = Field(..., description='The Name of the target table.')


class QueryVisualTopNExpression(BaseModel):
    
    ItemCount: float


class SortDirection(RootModel):
    root: Literal[1, 2]


class StandaloneSourceRefExpression(BaseModel):        

    Schema: str | None = Field(
        None,
        description='The name of the schema containing the referenced entity - can be omitted if optional.',
    )
    Entity: str = Field(
        ..., description='Name of the referenced entity from your data.'
    )


class TimeUnit(RootModel):
    root: Literal[0, 1, 2, 3, 4, 5, 6, 7]