"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import KathreinWallboxEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import WallboxDataUpdateCoordinator
    from .data import KathreinWallboxConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="integration_blueprint",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: KathreinWallboxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        KathreinWallboxSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class KathreinWallboxSensor(KathreinWallboxEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        coordinator: WallboxDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")
