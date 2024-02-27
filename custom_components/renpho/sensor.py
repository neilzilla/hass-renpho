"""Platform for sensor integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import slugify
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
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
        RenphoSensor(hass.data[DOMAIN], **sensor, config_entry=config_entry)
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
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
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


class RenphoSensor(SensorEntity, CoordinatorEntity):
    """Representation of a Renpho sensor."""

    def __init__(
        self,
        coordinator,
        renpho: RenphoWeight,
        id: str,
        name: str,
        unit: str,
        category: str,
        label: str,
        metric: str,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self._renpho = renpho
        self._metric = metric
        self._id = id
        self._name = f"Renpho {name}"
        self._unit = unit
        self._category = category
        self._label = label
        self._unit_of_measurement = config_entry.options.get(
            CONF_UNIT_OF_MEASUREMENT, MASS_KILOGRAMS
        )
        self._timestamp = None

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
        # Return the state of the sensor with correct unit conversion
        metric_value = self.coordinator.data.get(self._metric, {}).get(self._id)
        if metric_value is not None:
            if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS:
                return metric_value * KG_TO_LBS
            return metric_value
        return None

    @property
    def unit_of_measurement(self) -> str:
        # Return the correct unit of measurement based on user configuration
        return (
            MASS_POUNDS if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS else MASS_KILOGRAMS
        )

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
                metric_type=self._metric, metric=self._id, user_id=None
            )

            # Check if metric_value is None
            if metric_value is None:
                return

            # Update the coordinator data
            if self._unit_of_measurement == MASS_POUNDS and self._unit == MASS_KILOGRAMS:
                metric_value *= KG_TO_LBS

            self.coordinator.data[self._metric][self._id] = metric_value

            # Update the timestamp
            self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            _LOGGER.info(
                f"Successfully updated {self._name} for metric type {self._metric}"
            )

        except (ConnectionError, TimeoutError) as e:
            _LOGGER.error(
                f"{type(e).__name__} occurred while updating {self._name} for metric type {self._metric}: {e}"
            )

        except Exception as e:
            _LOGGER.critical(
                f"An unexpected error occurred while updating {self._name} for metric type {self._metric}: {e}"
            )
