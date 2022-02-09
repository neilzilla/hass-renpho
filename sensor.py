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
    async_add_entities([WeightSensor(coordinator), TimeSensor(coordinator), FatFreeWeightSensor(coordinator), SkeletalMuscalSensor(coordinator), ProteinSensor(coordinator), 
                 SinewSensor(coordinator), BmiSensor(coordinator), SubFatSensor(coordinator), VisceralFatSensor(coordinator), BoneSensor(coordinator), BodyAgeSensor(coordinator), 
                 BmrSensor(coordinator), WaterSensor(coordinator), BodyfatSensor(coordinator)], True)

class WeightSensor(CoordinatorEntity):
    """Weight sensor"""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0  #Ca sert à quelque chose ?

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Weight"

    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.weight
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            _temp_value = round(_temp_value * KG_TO_LB_MULTIPLICATOR, 1)

        self.attrs["weight"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value

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





class TimeSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        
        return f"Renpho {self.coordinator.data.account_name} Last Weighed Timestamp"

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return 'mdi:calendar-range'
		
    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        
        return ''
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.created_at
        self.attrs["created_at"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        return _temp_value

    @property
    def extra_state_attributes(self):
        return self.attrs

class FatFreeWeightSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Fat Free Weight"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self.coordinator.data.unit_of_measurements

    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.fat_free_weight
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            _temp_value = round(_temp_value * KG_TO_LB_MULTIPLICATOR, 1)

        self.attrs["fat_free_weight"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value

    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            return "mdi:weight-pound"

        return "mdi:weight-kilogram"

    @property
    def extra_state_attributes(self):
        return self.attrs

class SkeletalMuscalSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Skeletal Muscle Weight"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.muscle
        self.attrs["muscle"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs

class ProteinSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0
		
    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Protein sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.protein
        self.attrs["protein"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs
		
class SinewSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Muscle Mass sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self.coordinator.data.unit_of_measurements
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.sinew
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            _temp_value = round(_temp_value * KG_TO_LB_MULTIPLICATOR, 1)

        self.attrs["sinew"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            return "mdi:weight-pound"

        return "mdi:weight-kilogram"
    
    @property
    def extra_state_attributes(self):
        return self.attrs
		
class BmiSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} BMI sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ''
    
    @property
    def state(self):
        """Return the state of the sensor."""
        _temp_value = self.coordinator.data.bmi
        self.attrs["bmi"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs
		
class SubFatSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} SubFat sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.subfat
        self.attrs["subfat"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs
		
class VisceralFatSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Visceral Fat sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ''
    
    @property
    def state(self):
        """Return the state of the sensor."""

        _temp_value = self.coordinator.data.visfat
        self.attrs["visfat"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs
		
class BoneSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Bone Mass sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self.coordinator.data.unit_of_measurements
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.bone
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            _temp_value = round(_temp_value * KG_TO_LB_MULTIPLICATOR, 1)

        self.attrs["bone"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        if self.coordinator.data.unit_of_measurements != MASS_KILOGRAMS : 
            return "mdi:weight-pound"

        return "mdi:weight-kilogram"		
    
    @property
    def extra_state_attributes(self):
        return self.attrs

class BodyAgeSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Body Age sensor"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return 'years'
    
    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        return "mdi:account-box-outline"
    
    @property
    def state(self):
        """Return the state of the sensor."""

        _temp_value = self.coordinator.data.bodyage
        self.attrs["bodyage"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs

class BmrSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} BMR sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return 'kcal'
    
    @property
    def state(self):
        """Return the state of the sensor."""
                
        _temp_value = self.coordinator.data.bmr
        self.attrs["bmr"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs

class WaterSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Water sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE
    
    @property
    def icon(self):
        """Icon to use in the frontend."""
        
        return "mdi:water"
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.water
        self.attrs["water"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs

class BodyfatSensor(CoordinatorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator[Measurements]):
        super().__init__(coordinator)
        self.attrs = {}
        self._state = 0

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Renpho {self.coordinator.data.account_name} Body Fat sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE
    
    @property
    def state(self):
        """Return the state of the sensor."""
        
        _temp_value = self.coordinator.data.bodyfat
        self.attrs["bodyfat"] = _temp_value
        self.attrs["account_name"] = self.coordinator.data.account_name
        self.attrs["created_at"] = self.coordinator.data.created_at
        return _temp_value
    
    @property
    def extra_state_attributes(self):
        return self.attrs