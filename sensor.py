"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.const import MASS_KILOGRAMS, PERCENTAGE
from .types import Measurements
from .const import KG_TO_LB_MULTIPLICATOR, DOMAIN
import logging
from homeassistant import core
from homeassistant.util import slugify
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: core.HomeAssistant, config, async_add_entities, discovery_info=None
):
    """Setup the sensor platform."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([WeightSensor(coordinator)], True)

class WeightSensor(CoordinatorEntity):
    """Weight sensor"""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Weight"

    @property
    def state(self):
        """Return the state of the sensor."""
        #Todo : supprimer l'entite renpho.weight.2
        _weight = self.coordinator.data.weight
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            _weight = round(_weight * KG_TO_LB_MULTIPLICATOR, 1)

        self.attrs["weight"] = _weight
        self.attrs["account_name"] = self.coordinator.data.account_name
        return _weight

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        
        return self.coordinator.data.unit_of_measurements

    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            return "mdi:weight-pound"

        return "mdi:weight-kilogram"

    #TODO : Nécessaire ?
    @property
    def extra_state_attributes(self):
        return self.attrs
       