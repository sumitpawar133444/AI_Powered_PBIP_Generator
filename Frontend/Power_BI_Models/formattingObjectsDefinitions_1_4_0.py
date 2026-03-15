from __future__ import annotations
from pydantic import BaseModel, RootModel, Field, ConfigDict
from typing import Any, Literal

from Frontend.Power_BI_Models.semanticQuery_1_3_0 import QueryExpressionContainer

class DataRepetitionSelector(BaseModel):

    scopeId: QueryExpressionContainer | None = Field(
        None,
        description='Defines the intersection of scopes. For example - product color = red.',
    )
    wildcard: list[QueryExpressionContainer] | None = Field(
        None,
        description='Defines a match against all instances of a given DataView scope. Does not match Subtotals.\nDeprecated: - Use roles instead.',
    )
    roles: list[str] | None = Field(
        None, description='Matches against all fields in a role.'
    )
    total: list[QueryExpressionContainer] | None = Field(
        None, description='Matches against the totals and subtotals.'
    )
    dataViewWildcard: 'DataViewWildcard | None' = Field(
        None, description='Matches all instances or all totals or both.'
    )


class DataViewObjectDefinition(BaseModel):

    selector: 'Selector | None' = None
    properties: 'DataViewObjectPropertyDefinitions'


class DataViewObjectDefinitions(RootModel):
    root: dict[str, list[DataViewObjectDefinition]] | None = None


class DataViewObjectPropertyDefinitions(RootModel):
    root: dict[str, Any] | None = None


class DataViewWildcard(BaseModel):

    matchingOption: 'DataViewWildcardMatchingOption' = Field(
        ..., description='Defines the matching option to use.'
    )


class DataViewWildcardMatchingOption(RootModel):
    root: Literal[0, 1, 2]


class Selector(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # ADD THIS

    data: list[DataRepetitionSelector] | None = Field(
        None, description='Scope is defined by data bound to the visual.'
    )
    metadata: str | None = Field(
        None, description='Defines the scope to a specific field.'
    )
    id: str | None = Field(None, description='User defined scope.')
    highlightMatching: float | None = Field(
        0,
        description='Describes how the Selector should behave towards Highlighted Values within the Scope matched by that Selector.',
    )
    hierarchyMatching: float | None = Field(
        0,
        description='Describes how the selector matches hierarchy values.\nThis also changes how the query is generated for {@link DataViewScopeWildcard} selectors.\nNow those selectors can produce scopedValues for the level those match.\n\nThere are two ways that we can match values in the hierarchy:\n1.',
    )
    order: float | None = Field(
        None,
        description='Specifies a user-defined ordering of identical properties.\nSelector constructors should strive to monitonically increase this number across identical properties differing by id.',
    )