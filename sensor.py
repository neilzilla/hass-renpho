"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import MASS_KILOGRAMS, PERCENTAGE
from .const import KG_TO_LB_MULTIPLICATOR
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD_HASH


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""

    renpho = hass.data[DOMAIN]

    add_entities([WeightSensor(renpho), TimeSensor(renpho), FatFreeWeightSensor(renpho), SkeletalMuscalSensor(renpho), ProteinSensor(renpho), 
                 SinewSensor(renpho), BmiSensor(renpho), SubFatSensor(renpho), VisceralFatSensor(renpho), BoneSensor(renpho), BodyAgeSensor(renpho), 
                 BmrSensor(renpho), WaterSensor(renpho), BodyfatSensor(renpho)])


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
        return self._renpho.unit_of_measurements

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        self._state = self._renpho.weight
        if self._renpho.unit_of_measurements != MASS_KILOGRAMS : 
            self._state = round(self._renpho.weight * KG_TO_LB_MULTIPLICATOR, 1)
        

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
        return ''

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.created_at
        

class FatFreeWeightSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Fat Free Weight'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._renpho.unit_of_measurements

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        self._state = self._renpho.fat_free_weight
        if self._renpho.unit_of_measurements != MASS_KILOGRAMS : 
            self._state = round(self._renpho.fat_free_weight * KG_TO_LB_MULTIPLICATOR, 1)


class SkeletalMuscalSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Skeletal Muscle Weight'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.muscle


class ProteinSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Protein sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.protein

class SinewSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Muscle Mass sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._renpho.unit_of_measurements

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.sinew
        if self._renpho.unit_of_measurements != MASS_KILOGRAMS : 
            self._state = round(self._renpho.sinew * KG_TO_LB_MULTIPLICATOR, 1)

class BmiSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho BMI sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ''

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.bmi

class SubFatSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho SubFat sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.subfat

class VisceralFatSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Visceral Fat sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.visfat


class BoneSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Bone Mass sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._renpho.unit_of_measurements

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.bone
        if self._renpho.unit_of_measurements != MASS_KILOGRAMS : 
            self._state = round(self._renpho.bone * KG_TO_LB_MULTIPLICATOR, 1)


class BodyAgeSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Body Age sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return 'years'

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.bodyage


class BmrSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho BMR sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ''

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.bmr


class WaterSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Water sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.water


class BodyfatSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, renpho) -> None:
        """Initialize the sensor."""
        self._renpho = renpho
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Renpho Body Fat sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._renpho.bodyfat