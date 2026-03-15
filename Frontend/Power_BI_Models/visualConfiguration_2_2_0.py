from __future__ import annotations
from pydantic import BaseModel, RootModel, Field
from typing import Any, Literal
from enum import Enum

from Frontend.Power_BI_Models.formattingObjectsDefinitions_1_4_0 import DataViewObjectDefinitions, Selector
from Frontend.Power_BI_Models.semanticQuery_1_3_0 import QueryExpressionContainer

class AIDecompositionMethod(Enum):
    BestSplit = 'BestSplit'
    MaxSplit = 'MaxSplit'
    MinSplit = 'MinSplit'


class AILevelInformation(BaseModel):

    method: AIDecompositionMethod = Field(..., description='Type of expansion.')
    disabled: bool | None = Field(None, description='Is the level disabled.')


class Background(BaseModel):

    show: Any | None = None
    color: Any | None = None
    transparency: Any | None = None


class BackgroundItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Background = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class Border(BaseModel):

    show: Any | None = None
    color: Any | None = None
    radius: Any | None = None
    width: Any | None = None


class BorderItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Border = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class Divider(BaseModel):

    ignorePadding: Any | None = None
    show: Any | None = None
    color: Any | None = None
    width: Any | None = None
    style: Any | None = None


class DividerItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Divider = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class DropShadow(BaseModel):

    show: Any | None = None
    preset: Any | None = None
    position: Any | None = None
    color: Any | None = None
    transparency: Any | None = None
    shadowSpread: Any | None = None
    shadowBlur: Any | None = None
    angle: Any | None = None
    shadowDistance: Any | None = None


class DropShadowItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: DropShadow = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class ExpansionState(BaseModel):

    roles: list[str] = Field(
        ...,
        description='Visual roles (projection names) that have individual points expanded.',
    )
    root: 'RootExpansionState | None' = Field(
        None,
        description='Defines the specific values that are expanded for each field in the hierarchy',
    )
    levels: list['LevelExpansionState'] | None = Field(
        None, description='Describes the fields participating in the expansion'
    )


class GeneralItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: 'VisualContainerGeneralFormattingObjects' = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class LevelExpansionState(BaseModel):

    identityKeys: list[QueryExpressionContainer] | None = Field(
        None, description='Describes the fields in the visual.'
    )
    isCollapsed: bool | None = Field(
        None,
        description="True if the entire field isn't expanded (i.e. false if only specific instances are expanded).",
    )
    queryRefs: list[str] = Field(
        ...,
        description='Which fields in the query does this relate to - must match a queryRef in the query.',
    )
    isPinned: bool | None = Field(None, description='Is the field pinned.')
    isLocked: bool | None = Field(
        None, description='Is the field locked (used for decomposition tree)'
    )
    AIInformation: AILevelInformation | None = Field(
        None,
        description='More information about how the expansion is done (used for decomposition tree)',
    )


class LockAspect(BaseModel):

    show: Any | None = None


class LockAspectItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: LockAspect = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class NodeExpansionState(BaseModel):

    identityValues: list[QueryExpressionContainer] = Field(
        ...,
        description='Describes the instances that are expanded.\nMust by Literal expressions.',
    )
    isToggled: bool | None = Field(
        False, description='True if the value is expanded.'
    )
    children: list['NodeExpansionState'] | None = Field(
        None, description='Child values in the hierarchy that are expanded'
    )


class Padding(BaseModel):

    top: Any | None = None
    bottom: Any | None = None
    left: Any | None = None
    right: Any | None = None


class PaddingItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Padding = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class ProjectionState(BaseModel):

    showAll: bool | None = Field(
        None, description='Show all values for all fields in this projection.'
    )
    projections: list['RoleProjection'] = Field(
        ..., description='Defines the fields and their properties for this visual role.'
    )
    fieldParameters: list['RoleFieldParameter'] | None = Field(
        None, description='Defines any field parameters used as projections.'
    )


class Query(BaseModel):

    sortDefinition: 'SortDefinition | None' = Field(
        None, description='Defines how the data should be sorted in a visual'
    )
    options: 'VisualQueryOptions | None' = Field(
        None,
        description='Specific options to apply when running the query. Applies to certain visuals only.',
    )
    queryState: dict[str, ProjectionState] = Field(
        ...,
        description='Describes how the data should be arranged and used in the visual.',
    )
    isDrillDisabled: bool | None = Field(
        None,
        description='Should drill be allowed in the visual - only used by specific custom visuals.',
    )


class QuerySort(BaseModel):

    field: QueryExpressionContainer = Field(..., description='Field to sort by')
    direction: 'SortDirection' = Field(
        ..., description='Direction of sort - ascending or descending.'
    )


class RoleFieldParameter(BaseModel):

    parameterExpr: QueryExpressionContainer = Field(
        ..., description='Defines the parameter field.'
    )
    index: float = Field(
        ...,
        description='Index at which parameter fields begin in the projections list.',
    )
    length: float | None = Field(
        None,
        description='Number of fields replaced by the parameter in the projections list.',
    )
    sortDirection: 'SortDirection | None' = Field(
        None,
        description= "If the sort direction is set, the visual is sorted by this field parameter.\nThe implication of a visual being sorted by a field parameter is as follows:\n- If none of the newly projected fields exist in the sort list, apply the parameter sort direction to the first projected field and add it to the end of the sort list.\n- If all the projected fields in the sort list have the opposite sort direction as the parameter's sort direction, flip the parameter's sort direction."
    )


class RoleProjection(BaseModel):

    field: QueryExpressionContainer = Field(
        ..., description='The data field from the semantic model.'
    )
    queryRef: str = Field(
        ..., description='A unique name for this field - unique per visual.'
    )
    nativeQueryRef: str | None = Field(
        None,
        description='Native reference name for this field - unique per visual, used for referencing fields in visual calculations.',
    )
    displayName: str | None = Field(
        None,
        description='An override for display name - by default it is the field name in the semantic model.',
    )
    format: str | None = Field(
        None, max_length=255, description='format string scoped to the visual.'
    )
    active: bool | None = Field(
        None,
        description='Is the field currently active in the visual - used as part of drill operations.',
    )
    hidden: bool | None = Field(
        None,
        description='Is the field visible in the visual - used as part of visual calculations.',
    )


class RootExpansionState(BaseModel):

    identityValues: list[QueryExpressionContainer] | None = Field(
        None,
        description='Describes the instances that are expanded.\nOptional for the root expansion state.\nMust by Literal expressions.',
    )
    isToggled: bool | None = Field(
        False, description='True if the value is expanded.'
    )
    children: list[NodeExpansionState] | None = Field(
        None, description='Child values in the hierarchy that are expanded'
    )


class SortDefinition(BaseModel):

    sort: list[QuerySort] | None = Field(
        None, description='Defines the fields the data is sorted by.'
    )
    isDefaultSort: bool | None = Field(
        None,
        description='If the sort if explicitly set by user, then this will be false, Power BI can update the sort to match\nthe visual in this case.',
    )


class SortDirection(RootModel):
    root: Literal["Ascending", "Descending"]


class Spacing(BaseModel):

    customizeSpacing: Any | None = None
    verticalSpacing: Any | None = None
    spaceBelowTitle: Any | None = None
    spaceBelowSubTitle: Any | None = None
    spaceBelowTitleArea: Any | None = None


class SpacingItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Spacing = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class StylePreset(BaseModel):

    name: Any | None = None


class StylePresetItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: StylePreset = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class SubTitle(BaseModel):

    show: Any | None = None
    text: Any | None = None
    heading: Any | None = None
    titleWrap: Any | None = None
    fontColor: Any | None = None
    alignment: Any | None = None
    fontSize: Any | None = None
    bold: Any | None = None
    italic: Any | None = None
    underline: Any | None = None
    fontFamily: Any | None = None


class SubTitleItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: SubTitle = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class Title(BaseModel):

    show: Any | None = None
    text: Any | None = None
    heading: Any | None = None
    titleWrap: Any | None = None
    fontColor: Any | None = None
    background: Any | None = None
    alignment: Any | None = None
    fontSize: Any | None = None
    bold: Any | None = None
    italic: Any | None = None
    underline: Any | None = None
    fontFamily: Any | None = None


class TitleItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: Title = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class VisualConfiguration(BaseModel):

    visualType: str = Field(..., description='Name of the visual.')
    autoSelectVisualType: bool | None = Field(
        None,
        description='VisualType is automatically picked by the system based on the data used in the visual.',
    )
    query: Query | None = Field(
        None, description='Defines the data to be plotted in the visual.'
    )
    expansionStates: list[ExpansionState] | None = Field(
        None, description='Defines the specific data points that are expanded.'
    )
    objects: DataViewObjectDefinitions | None = Field(
        None,
        description='Specifies the formatting to be set for different "objects" of the visual.',
    )
    visualContainerObjects: 'VisualContainerFormattingObjects | None' = Field(
        None,
        description='Specifies the formatting to be set for different "objects" of the container.',
    )
    syncGroup: 'VisualSyncGroup | None' = Field(
        None,
        description='Defines the sync group that this visual is part of.\nOnly applies to slicer visuals.',
    )
    drillFilterOtherVisuals: bool | None = Field(
        None,
        description='When another visual is drilled, if visual interactions are enabled between the two visuals,\nthen this property specifies if that drill should be applied as a filter to this visual.\nOverrides the default setting of the report.',
    )


class VisualContainerFormattingObjects(BaseModel):

    title: list[TitleItem] | None = None
    subTitle: list[SubTitleItem] | None = None
    divider: list[DividerItem] | None = None
    spacing: list[SpacingItem] | None = None
    background: list[BackgroundItem] | None = None
    padding: list[PaddingItem] | None = None
    lockAspect: list[LockAspectItem] | None = None
    general: list[GeneralItem] | None = None
    border: list[BorderItem] | None = None
    dropShadow: list[DropShadowItem] | None = None
    visualLink: list['VisualLinkItem'] | None = None
    visualTooltip: list['VisualTooltipItem'] | None = None
    stylePreset: list[StylePresetItem] | None = None
    visualHeader: list['VisualHeaderItem'] | None = None
    visualHeaderTooltip: list['VisualHeaderTooltipItem'] | None = None


class VisualContainerGeneralFormattingObjects(BaseModel):

    x: Any | None = None
    y: Any | None = None
    width: Any | None = None
    height: Any | None = None
    altText: Any | None = None
    allowBinnedLineSample: Any | None = None
    allowOverlappingPointsSample: Any | None = None
    keepLayerOrder: Any | None = None


class VisualHeader(BaseModel):

    show: Any | None = None
    background: Any | None = None
    border: Any | None = None
    transparency: Any | None = None
    foreground: Any | None = None
    showVisualInformationButton: Any | None = None
    showVisualWarningButton: Any | None = None
    showVisualErrorButton: Any | None = None
    showDrillRoleSelector: Any | None = None
    showDrillUpButton: Any | None = None
    showDrillToggleButton: Any | None = None
    showDrillDownLevelButton: Any | None = None
    showDrillDownExpandButton: Any | None = None
    showPinButton: Any | None = None
    showFilterRestatementButton: Any | None = None
    showFocusModeButton: Any | None = None
    showCopyVisualImageButton: Any | None = None
    showSeeDataLayoutToggleButton: Any | None = None
    showOptionsMenu: Any | None = None
    showCommentButton: Any | None = None
    showTooltipButton: Any | None = None
    showPersonalizeVisualButton: Any | None = None
    showSmartNarrativeButton: Any | None = None
    showSetAlertButton: Any | None = None
    showFollowVisualButton: Any | None = None


class VisualHeaderItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: VisualHeader = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class VisualHeaderTooltip(BaseModel):

    type: Any | None = None
    section: Any | None = None
    text: Any | None = None
    titleFontColor: Any | None = None
    fontSize: Any | None = None
    fontFamily: Any | None = None
    bold: Any | None = None
    italic: Any | None = None
    underline: Any | None = None
    background: Any | None = None
    transparency: Any | None = None
    themedTitleFontColor: Any | None = None
    themedBackground: Any | None = None


class VisualHeaderTooltipItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: VisualHeaderTooltip = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class VisualLink(BaseModel):

    show: Any | None = None
    type: Any | None = None
    bookmark: Any | None = None
    disabledTooltip: Any | None = None
    drillthroughSection: Any | None = None
    enabledTooltip: Any | None = None
    qna: Any | None = None
    suppressDefaultTooltip: Any | None = None
    showDefaultTooltip: Any | None = None
    navigationSection: Any | None = None
    tooltip: Any | None = None
    tooltipPlaceholderText: Any | None = None
    webUrl: Any | None = None
    dataFunction: Any | None = None


class VisualLinkItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: VisualLink = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )


class VisualQueryOptions(BaseModel):

    allowBinnedLineSample: bool | None = Field(
        None, description='A better sampling for line charts.'
    )
    allowOverlappingPointsSample: bool | None = Field(
        None, description='A better sampling for scatter charts.'
    )


class VisualSyncGroup(BaseModel):

    groupName: str = Field(..., description='Unique name for the sync group.')
    fieldChanges: bool | None = Field(
        None, description='Should synced visuals update when fields change.'
    )
    filterChanges: bool | None = Field(
        None, description='Should synced visuals update when filters change.'
    )


class VisualTooltip(BaseModel):

    show: Any | None = None
    type: Any | None = None
    section: Any | None = None
    titleFontColor: Any | None = None
    valueFontColor: Any | None = None
    fontSize: Any | None = None
    bold: Any | None = None
    italic: Any | None = None
    underline: Any | None = None
    fontFamily: Any | None = None
    background: Any | None = None
    transparency: Any | None = None
    actionFontColor: Any | None = None
    themedTitleFontColor: Any | None = None
    themedBackground: Any | None = None
    themedValueFontColor: Any | None = None


class VisualTooltipItem(BaseModel):

    selector: Selector | None = Field(
        None,
        description='Defines the scope at which to apply the formatting for this object.\nCan also define rules for matching highlighted values and how multiple definitions for the same property should be ordered.',
    )
    properties: VisualTooltip = Field(
        ...,
        description='Describes the properties of the object to apply formatting changes to.',
    )