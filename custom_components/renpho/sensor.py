"""Platform for sensor integration."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import slugify
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_REFRESH,
    CONF_UNIT_OF_MEASUREMENT,
    DOMAIN,
    KG_TO_LBS,
    MASS_KILOGRAMS,
    MASS_POUNDS,
)
from .api_renpho import _LOGGER, RenphoWeight
from .sensor_configs import sensor_configurations


async def sensors_list(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> list[RenphoSensor]:
    """Return a list of sensors."""
    return [
        RenphoSensor(hass.data[DOMAIN], **sensor, unit_of_measurement=hass.data[CONF_UNIT_OF_MEASUREMENT])
        for sensor in sensor_configurations
    ]


async def async_setup(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    sensor_entities = await sensors_list(hass, config_entry)
    async_add_entities(sensor_entities)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):

    sensor_entities = await sensors_list(hass, config_entry)
    async_add_entities(sensor_entities)
    return True


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
):
    """Set up the sensor platform asynchronously."""
    sensor_entities = await sensors_list(hass, discovery_info)
    async_add_entities(sensor_entities)


class RenphoSensor(SensorEntity):
    """Representation of a Renpho sensor."""

    def __init__(
        self,
        renpho: RenphoWeight,
        id: str,
        name: str,
        unit: str,
        category: str,
        label: str,
        metric: str,
        unit_of_measurement: str,
    ) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._metric = metric
        self._id = id
        self._name = f"Renpho {name}"
        self._unit = unit
        self._category = category
        self._label = label
        self._unit_of_measurement = unit_of_measurement
        self._timestamp = None
        self._state = None

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"renpho_{slugify(self._name)}"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "timestamp": self._timestamp,
            "category": self._category,
            "label": self._label,
        }

    @property
    def extra_state_attributes(self):
        # Updated property name for HA compatibility
        return {
            "timestamp": self._timestamp,
            "category": self._category,
            "label": self._label,
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        """Return the current state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        # Return the correct unit of measurement based on user configuration
        if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS:
            return MASS_POUNDS
        elif self._unit_of_measurement == MASS_KILOGRAMS and self._unit == MASS_KILOGRAMS:
            return MASS_KILOGRAMS
        elif self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_POUNDS:
            return MASS_POUNDS
        elif self._unit_of_measurement == MASS_KILOGRAMS or MASS_POUNDS and self._unit != MASS_KILOGRAMS or MASS_POUNDS:
            return self._unit

    @property
    def unit(self) -> str:
        """Return the unit of the sensor."""
        if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS:
            return MASS_POUNDS
        elif self._unit_of_measurement == MASS_KILOGRAMS and self._unit == MASS_KILOGRAMS:
            return MASS_KILOGRAMS
        elif self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_POUNDS:
            return MASS_POUNDS
        elif self._unit_of_measurement == MASS_KILOGRAMS or MASS_POUNDS and self._unit != MASS_KILOGRAMS or MASS_POUNDS:
            return self._unit

    @property
    def category(self) -> str:
        """Return the category of the sensor."""
        return self._category

    @property
    def label(self) -> str:
        """Return the label of the sensor."""
        return self._label

    async def async_update(self) -> None:
        try:
            metric_value = await self._renpho.get_specific_metric(
                metric_type=self._metric,
                metric=self._id,
                user_id=None
            )

            if metric_value is not None:
                if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS:
                    self._state = round(metric_value * KG_TO_LBS, 2)
                elif self._unit_of_measurement == MASS_KILOGRAMS and self._unit == MASS_KILOGRAMS:
                    self._state = round(metric_value, 2)
                else:
                    self._state = metric_value
                self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                _LOGGER.info(f"Successfully updated {self._name} for metric type {self._metric} with value {self._state} with unit {self._unit}")
            else:
                self._state = None  # You might choose to clear the state or leave it unchanged

        except (ConnectionError, TimeoutError) as e:
            _LOGGER.error(
                f"{type(e).__name__} occurred while updating {self._name} for metric type {self._metric}: {e}"
            )

        except Exception as e:
            _LOGGER.critical(
                f"An unexpected error occurred while updating {self._name} for metric type {self._metric}: {e}"
            )
