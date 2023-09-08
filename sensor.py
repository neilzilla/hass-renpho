"""Platform for sensor integration."""
from __future__ import annotations
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.util import slugify
from homeassistant.core import callback

from homeassistant.const import MASS_KILOGRAMS, TIME_SECONDS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .RenphoWeight import _LOGGER
from .const import CM_TO_INCH, DOMAIN, CONF_EMAIL, CONF_PASSWORD, KG_TO_LBS


# Existing setup_platform function
def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the sensor platform."""

    renpho = hass.data[DOMAIN]

    # sensor_configurations = []
    # entities = [RenphoSensor(renpho, *config) for config in sensor_configurations]
    # add_entities(entities)

    add_entities(
        [
            # Physical Metrics
            RenphoSensor(renpho, "weight", "Weight", "kg", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "bmi", "BMI", "", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "muscle", "Muscle Mass", "%", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "bone", "Bone Mass", "%", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "waistline", "Waistline", "cm", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "hip", "Hip", "cm", category="Measurements", label="Physical Metrics"),
            RenphoSensor(renpho, "stature", "Stature", "cm", category="Measurements", label="Physical Metrics"),

            # Body Composition
            RenphoSensor(renpho, "bodyfat", "Body Fat", "%", category="Measurements", label="Body Composition"),
            RenphoSensor(renpho, "water", "Water Content", "%", category="Measurements", label="Body Composition"),
            RenphoSensor(renpho, "subfat", "Subcutaneous Fat", "%", category="Measurements", label="Body Composition"),
            RenphoSensor(renpho, "visfat", "Visceral Fat", "Level", category="Measurements", label="Body Composition"),

            # Metabolic Metrics
            RenphoSensor(renpho, "bmr", "BMR", "kcal/day", category="Measurements", label="Metabolic Metrics"),
            RenphoSensor(renpho, "protein", "Protein Content", "%", category="Measurements", label="Metabolic Metrics"),

            # Age Metrics
            RenphoSensor(renpho, "bodyage", "Body Age", "Years", category="Measurements", label="Age Metrics"),

            # Device Information
            RenphoSensor(renpho, "mac", "MAC Address", "", category="Device", label="Device Information"),
            RenphoSensor(renpho, "scale_type", "Scale Type", "", category="Device", label="Device Information"),
            RenphoSensor(renpho, "scale_name", "Scale Name", "", category="Device", label="Device Information"),

            # Miscellaneous
            RenphoSensor(renpho, "method", "Measurement Method", "", category="Miscellaneous", label="Additional Metrics"),
            RenphoSensor(renpho, "pregnant_flag", "Pregnant Flag", "", category="Miscellaneous", label="Additional Metrics"),
            RenphoSensor(renpho, "sport_flag", "Sport Flag", "", category="Miscellaneous", label="Additional Metrics"),
            RenphoSensor(renpho, "score", "Score", "", category="Miscellaneous", label="Additional Metrics"),
            RenphoSensor(renpho, "remark", "Remark", "", category="Miscellaneous", label="Additional Metrics"),

            # Meta Information
            RenphoSensor(renpho, "id", "Record ID", "", category="Meta", label="Meta Information"),
            RenphoSensor(renpho, "b_user_id", "User ID", "", category="Meta", label="Meta Information"),
            RenphoSensor(renpho, "time_stamp", "Time Stamp", "UNIX Time", category="Meta", label="Meta Information"),
            RenphoSensor(renpho, "created_at", "Created At", "", category="Meta", label="Meta Information"),

            # User Profile
            RenphoSensor(renpho, "gender", "Gender", "", category="User", label="User Profile"),
            RenphoSensor(renpho, "height", "Height", "cm", category="User", label="User Profile"),
            RenphoSensor(renpho, "birthday", "Birthday", "", category="User", label="User Profile"),

            # Electrical Measurements
            RenphoSensor(renpho, "resistance", "Electrical Resistance", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "sec_resistance", "Secondary Electrical Resistance", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "actual_resistance", "Actual Electrical Resistance", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "actual_sec_resistance", "Actual Secondary Electrical Resistance", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance20_left_arm", "Resistance20 Left Arm", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance20_left_leg", "Resistance20 Left Leg", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance20_right_arm", "Resistance20 Right Arm", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance20_right_leg", "Resistance20 Right Leg", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance20_trunk", "Resistance20 Trunk", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance100_left_arm", "Resistance100 Left Arm", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance100_left_leg", "Resistance100 Left Leg", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance100_right_arm", "Resistance100 Right Arm", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance100_right_leg", "Resistance100 Right Leg", "Ohms", category="Measurements", label="Electrical Measurements"),
            RenphoSensor(renpho, "resistance100_trunk", "Resistance100 Trunk", "Ohms", category="Measurements", label="Electrical Measurements"),


            # Cardiovascular Metrics
            RenphoSensor(renpho, "heart_rate", "Heart Rate", "bpm", category="Measurements", label="Cardiovascular Metrics"),
            RenphoSensor(renpho, "cardiac_index", "Cardiac Index", "", category="Measurements", label="Cardiovascular Metrics"),

            # Other Metrics
            RenphoSensor(renpho, "method", "Method Used", "", category="Miscellaneous", label="Other Metrics"),
            RenphoSensor(renpho, "sport_flag", "Sports Flag", "", category="Miscellaneous", label="Other Metrics"),
            RenphoSensor(renpho, "left_weight", "Left Weight", "kg", category="Measurements", label="Other Metrics"),
            RenphoSensor(renpho, "right_weight", "Right Weight", "kg", category="Measurements", label="Other Metrics"),
            RenphoSensor(renpho, "local_created_at", "Local Created At", "", category="Meta", label="Other Metrics"),
            RenphoSensor(renpho, "time_zone", "Time Zone", "", category="Device", label="Other Metrics"),
            RenphoSensor(renpho, "remark", "Additional Remarks", "", category="Miscellaneous", label="Other Metrics"),
            RenphoSensor(renpho, "score", "Health Score", "", category="Miscellaneous", label="Other Metrics"),
            RenphoSensor(renpho, "pregnant_flag", "Pregnancy Flag", "", category="Miscellaneous", label="Other Metrics"),
            RenphoSensor(renpho, "stature", "Stature Information", "cm", category="Measurements", label="Other Metrics"),
            RenphoSensor(renpho, "category", "Category Identifier", "", category="Miscellaneous", label="Other Metrics"),
        ]
    )



class RenphoSensor(SensorEntity):
    def __init__(
            self, renpho, metric, name, unit_of_measurement, category="Renpho", label="Data", convert_unit=False) -> None:
        self._renpho = renpho
        self._metric = metric
        self._name = f"Renpho {name}"
        self._unit_of_measurement = unit_of_measurement
        self._category = category
        self._label = label
        self._state = None
        self._convert_unit = convert_unit
        self._timestamp = None

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"renpho_{slugify(self._name)}"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            'timestamp': self._timestamp,
            'category': self._category,
            'label': self._label
        }

    # Conversion method for kg to lbs
    def kg_to_lbs(self, kg):
        return kg * KG_TO_LBS

    # Conversion method for cm to inch
    def cm_to_inch(self, cm):
        return cm * CM_TO_INCH

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        """ Return the state of the sensor.
            If the unit is kg or cm, convert to lbs or inch respectively.

        """
        if self._convert_unit:
            if self._unit_of_measurement == MASS_KILOGRAMS:
                return self.kg_to_lbs(self._state)
            elif self._unit_of_measurement == "cm":
                return self.cm_to_inch(self._state)
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """ Return the unit of measurement.
            If the unit is kg or cm, convert to lbs or inch respectively.

        """
        if self._convert_unit:
            if self._unit_of_measurement == MASS_KILOGRAMS:
                return "lbs"
            elif self._unit_of_measurement == "cm":
                return "inch"
        return self._unit_of_measurement

    @property
    def category(self) -> str:
        """ Return the category of the sensor. """
        return self._category

    @property
    def label(self) -> str:
        """ Return the label of the sensor. """
        return self._label

    def update(self):
        """ Update the sensor using the event loop for asynchronous code. """
        self.hass.async_add_job(self._async_internal_update())

    @callback
    async def _async_internal_update(self):
        """ Internal method to update the sensor asynchronously. """
        try:
            metric_value = await self._renpho.getSpecificMetric(self._metric)  # Assuming asynchronous version
            if metric_value is not None:
                self._state = metric_value
                self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                _LOGGER.info(f"Successfully updated {self._name}")
            else:
                _LOGGER.warning(f"{self._metric} returned None. Not updating {self._name}.")
        except (ConnectionError, TimeoutError) as e:
            _LOGGER.error(f"{type(e).__name__} updating {self._name}: {e}")
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred updating {self._name}: {e}")

