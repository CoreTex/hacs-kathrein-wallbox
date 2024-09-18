"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfTime,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import CHARGING_CURRENTS, DOMAIN, DYNAMIC_UNIT

from .entity import KathreinWallboxEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import WallboxDataUpdateCoordinator
    from .data import KathreinWallboxConfigEntry

SENSOR_DESCRIPTIONS: Final[tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        key="_total_driving_range",
        name="Total Driving Range",
        icon="mdi:road-variant",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="_odometer",
        name="Odometer",
        icon="mdi:speedometer",
        native_unit_of_measurement=DYNAMIC_UNIT,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="_last_service_distance",
        name="Last Service",
        icon="mdi:car-wrench",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="_next_service_distance",
        name="Next Service",
        icon="mdi:car-wrench",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="car_battery_percentage",
        name="Car Battery Level",
        icon="mdi:car-battery",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="last_updated_at",
        name="Last Updated At",
        icon="mdi:update",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="ev_battery_percentage",
        name="EV Battery Level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ev_battery_soh_percentage",
        name="EV State of Health Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    SensorEntityDescription(
        key="ev_battery_remain",
        name="EV Battery Level",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ev_battery_capacity",
        name="EV Battery Capacity",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="_ev_driving_range",
        name="EV Range",
        icon="mdi:road-variant",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="_fuel_driving_range",
        name="Fuel Driving Range",
        icon="mdi:road-variant",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="fuel_level",
        name="Fuel Level",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fuel",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="_air_temperature",
        name="Set Temperature",
        native_unit_of_measurement=DYNAMIC_UNIT,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key="ev_estimated_current_charge_duration",
        name="Estimated Charge Duration",
        icon="mdi:ev-station",
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    SensorEntityDescription(
        key="ev_estimated_fast_charge_duration",
        name="Estimated Fast Charge Duration",
        icon="mdi:ev-station",
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    SensorEntityDescription(
        key="ev_estimated_portable_charge_duration",
        name="Estimated Portable Charge Duration",
        icon="mdi:ev-station",
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    SensorEntityDescription(
        key="ev_estimated_station_charge_duration",
        name="Estimated Station Charge Duration",
        icon="mdi:ev-station",
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    SensorEntityDescription(
        key="_ev_target_range_charge_AC",
        name="Target Range of Charge AC",
        icon="mdi:ev-station",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="_ev_target_range_charge_DC",
        name="Target Range of Charge DC",
        icon="mdi:ev-station",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DYNAMIC_UNIT,
    ),
    SensorEntityDescription(
        key="total_power_consumed",
        name="Total Energy Consumption",
        icon="mdi:car-electric",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="total_power_regenerated",
        name="Total Energy Regeneration",
        icon="mdi:car-electric",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Need to remove km hard coding.  Underlying API needs this fixed first.  EU always does KM.
    SensorEntityDescription(
        key="power_consumption_30d",
        name="Average Energy Consumption",
        icon="mdi:car-electric",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{UnitOfEnergy.WATT_HOUR}/km",
    ),
    SensorEntityDescription(
        key="front_left_seat_status",
        name="Front Left Seat",
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="front_right_seat_status",
        name="Front Right Seat",
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="rear_left_seat_status",
        name="Rear Left Seat",
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="rear_right_seat_status",
        name="Rear Right Seat",
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="_geocode_name",
        name="Geocoded Location",
        icon="mdi:map",
    ),
    SensorEntityDescription(
        key="dtc_count",
        name="DTC Count",
        icon="mdi:alert-circle",
    ),
    SensorEntityDescription(
        key="ev_first_departure_time",
        name="EV First Scheduled Departure Time",
        icon="mdi:clock-outline",
    ),
    SensorEntityDescription(
        key="ev_second_departure_time",
        name="EV Second Scheduled Departure Time",
        icon="mdi:clock-outline",
    ),
    SensorEntityDescription(
        key="ev_off_peak_start_time",
        name="EV Off Peak Start Time",
        icon="mdi:clock-outline",
    ),
    SensorEntityDescription(
        key="ev_off_peak_end_time",
        name="EV Off Peak End Time",
        icon="mdi:clock-outline",
    ),
    SensorEntityDescription(
        key="ev_v2l_discharge_limit",
        name="V2L Discharge Limit",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    SensorEntityDescription(
        key="ev_charging_current",
        name="Charging Current Limit",
        icon="mdi:lightning-bolt-circle",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.POWER_FACTOR,
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
        for entity_description in SENSOR_DESCRIPTIONS
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
