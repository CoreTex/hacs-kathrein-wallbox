"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import KathreinWallboxApiClient
    from .coordinator import WallboxDataUpdateCoordinator


type KathreinWallboxConfigEntry = ConfigEntry[KathreinWallboxData]


@dataclass
class KathreinWallboxData:
    """Data for the Wallbox integration."""

    client: KathreinWallboxApiClient
    coordinator: WallboxDataUpdateCoordinator
    integration: Integration
