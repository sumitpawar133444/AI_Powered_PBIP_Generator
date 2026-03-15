from __future__ import annotations
from pydantic import BaseModel, RootModel, Field
from typing import Any, Literal

from Frontend.Power_BI_Models.visualConfiguration_2_2_0 import VisualConfiguration, BackgroundItem, LockAspectItem
from Frontend.Power_BI_Models.filterConfiguration_1_2_0 import FilterConfiguration
from Frontend.Power_BI_Models.formattingObjectsDefinitions_1_4_0 import Selector

class Annotation(BaseModel):

    name: str = Field(..., description='Unique name for the annotation.')
    value: str = Field(..., description='A value for this annotation.')


class GeneralItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: 'VisualGroupGeneralFormattingObjects' = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class GroupLayoutMode(RootModel):
    root: Literal["ScaleMode", "ScrollMode"]


class HowCreated(RootModel):
    root: Literal[
            "Default",
            "Copilot",
            "CheckboxTickedInFieldList",
            "DraggedToCanvas",
            "VisualTypeIconClicked",
            "DraggedToFieldWell",
            "InsertVisualButton",
            "WhatIfParameterControl",
            "QnaAppBar",
            "QnaDoubleClick",
            "QnaKeyboardShortcut",
            "FieldParameterControl",
            "CanvasBackgroundContextMenu",
            "ContextMenuPaste",
            "CopyPaste",
            "SummarizeVisualContainer",
        ]


class VisualContainer(RootModel):

    root: 'VisualContainer1' = Field(
        ...,
        description='Defines a single visual or visual group on a report page.',
        title='Visual container',
    )


class VisualContainer1(BaseModel):

    field_schema: str = Field(
        'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.2.0/schema.json',
        alias='$schema',
        # const=True,
        description='Defines the schema to use for an item.',
    )
    name: str = Field(
        ..., max_length = 50, description='A unique identifier for the visual across the whole page.'
    )
    position: 'VisualContainerPosition' = Field(
        ...,
        description='Defines where the visual is position on the page and how big it should be, along\nwith z-index (stacking) for that visual.\nAlso defines the order in which visuals are navigated when using just keyboard (tabOrder).',
    )
    visual: VisualConfiguration = Field(
        ..., description='Defines a chart to be shown inside of this container.'
    )
    visualGroup: 'VisualGroupConfig | None' = Field(
        None,
        description='Defines that this container should be used as a grouping container.',
    )
    parentGroupName: str | None = Field(
        None,
        description='Name of the parent group (visual container), if it is part of one.',
    )
    filterConfig: FilterConfiguration | None = Field(
        None,
        description='Filters that apply to all this visual - on top of the filters defined for the report and page.',
    )
    isHidden: bool | None = Field(None, description='Marks the visual as hidden.')
    annotations: list[Annotation] | None = Field(
        None,
        description='Additional information to be saved (for example comments, readme, etc) for this visual.',
    )
    howCreated: HowCreated | None = Field(
        None, description='Source of creation of this visual.'
    )


class VisualContainerPosition(BaseModel):

    x: float = Field(
        ...,
        description='Horizontal position of the left edge of the visual.\nShould be between 0 and width of the containing page.',
    )
    y: float = Field(
        ...,
        description='Vertical position of the top edge of the visual.\nShould be between 0 and height of the containing page.',
    )
    z: float | None = Field(
        None,
        description='Defines the stacking order for the visual.\nHigher z-index visuals are shown on top of the lower ones.',
    )
    height: float = Field(
        ...,
        description='Height of the visual.\ny + height should be less than the height of the containing page.',
    )
    width: float = Field(
        ...,
        description='Width of the visual.\nx + width should be less than the width of the containing page.',
    )
    tabOrder: float | None = Field(
        None,
        description='Defines the selection order for this visual when using keyboard (tab key)\nto navigate the visuals on the containing page.',
    )
    angle: float | None = None


class VisualGroupConfig(BaseModel):

    displayName: str = Field(..., description='Display name for the group.')
    groupMode: GroupLayoutMode = Field(
        ..., description='Defines how the visuals are organized inside this group.'
    )
    objects: 'VisualGroupFormattingObjects | None' = Field(
        None,
        description='Specifies the formatting to be set for different "objects" of this group.',
    )


class VisualGroupFormattingObjects(BaseModel):

    background: list[BackgroundItem] | None = None
    lockAspect: list[LockAspectItem] | None = None
    general: list[GeneralItem] | None = None


class VisualGroupGeneralFormattingObjects(BaseModel):

    x: Any | None = None
    y: Any | None = None
    width: Any | None = None
    height: Any | None = None
    altText: Any | None = None

