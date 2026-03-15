from __future__ import annotations
from pydantic import BaseModel, RootModel, Field
from typing import Any, Literal

from Frontend.Power_BI_Models.formattingObjectsDefinitions_1_4_0 import Selector
from Frontend.Power_BI_Models.semanticQuery_1_3_0 import FilterDefinition, QueryExpressionContainer

class FilterConfiguration(BaseModel):

    filters: list['FilterContainer'] | None = Field(
        None, description='Defines the definitions and metadata for the filters.'
    )
    filterSortOrder: 'FilterSortOrder | None' = Field(
        None,
        description='Defines how the filters sorted - by name or custom sorting\nIf custom sorting, then ordinal property of every filter is used as the sort order,\nfilters where ordinal is skipped will be shown at the end; ordering will fallback to display name of the field.',
    )


class FilterContainer(BaseModel):

    name: str = Field(
        ...,
        description='A unique name (across the whole report definition) defined for this filter.',
    )
    displayName: str | None = Field(
        None,
        description='An alternate name to use when displaying this filter - by default the display name of the field will be used, if there is no field or display name,\nthen restatement of the filter will be shown. Only applies to certain filter types.',
    )
    ordinal: float | None = Field(
        None,
        description='Defines the ordering of this filter w.r.t. other filters - only applies when Custom sort order is set.',
    )
    field: QueryExpressionContainer | None = Field(
        None, description='Defines the field from your data that is filtered.'
    )
    type: str | None = Field(None, description='The type of a filter.')
    filter: FilterDefinition | None = Field(
        None,
        description='Defines the actual filter definition - it is dependent on the type of filter.',
    )
    restatement: str | None = Field(
        None,
        description='A custom restatement to show for the filter - only applies to Passthrough filter type. For all other filters, a restatement is generated based on the filter definition.',
    )
    howCreated: str | None = Field(
        None, description='Specifies how this filter was first created.'
    )
    isHiddenInViewMode: bool | None = Field(
        None, description='Defines whether to hide this filter when viewing the report.'
    )
    isLockedInViewMode: bool | None = Field(
        None,
        description='Defines whether the filter value can be changed when viewing the report.',
    )
    objects: 'FilterContainerFormattingObjects | None' = Field(
        None, description='Formatting for different "objects" of a filter card'
    )


class FilterContainerFormattingObjects(BaseModel):

    general: list['GeneralItem'] | None = None


class FilterContainerFormattingObjectsProperties(BaseModel):

    requireSingleSelect: Any | None = None
    isInvertedSelectionMode: Any | None = None


class FilterSortOrder(RootModel):
    root: Literal["Ascending", "Descending", "Custom"]


class GeneralItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: FilterContainerFormattingObjectsProperties = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )