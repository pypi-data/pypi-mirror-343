"""This module contains settings model for user preferences."""

from enum import Enum

from sqlmodel import Field, SQLModel


class GridViewSampleRenderingType(str, Enum):
    """Defines how samples are rendered in the grid view."""

    COVER = "cover"
    CONTAIN = "contain"


class SettingBase(SQLModel):
    """Base class for Settings model."""

    grid_view_sample_rendering: GridViewSampleRenderingType = Field(
        default=GridViewSampleRenderingType.CONTAIN,
        description="Controls how samples are rendered in the grid view",
    )
