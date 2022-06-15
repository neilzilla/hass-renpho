"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import MASS_KILOGRAMS, TIME_SECONDS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD




def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""

    renpho = hass.data[DOMAIN]

    add_entities([WeightSensor(renpho), TimeSensor(renpho)])


class WeightSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Weight'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return MASS_KILOGRAMS

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.weight

class TimeSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Last Weighed Timestamp'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TIME_SECONDS

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.time_stamp