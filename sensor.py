"""Platform for sensor integration."""
from __future__ import annotations
from datetime import datetime

from homeassistant.components.sensor import SensorEntity

from homeassistant.const import MASS_KILOGRAMS, TIME_SECONDS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from RenphoWeight import _LOGGER
from const import CM_TO_INCH, DOMAIN, CONF_EMAIL, CONF_PASSWORD, KG_TO_LBS


# Existing setup_platform function
def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the sensor platform."""

    renpho = hass.data[DOMAIN]

    # Adding entities with categories and labels
    add_entities(
        [
            # Measurements - Physical Metrics
            RenphoSensor(
                renpho,
                "weight",
                "Weight",
                MASS_KILOGRAMS,
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "bmi",
                "BMI",
                "",
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "muscle",
                "Muscle Mass",
                "%",
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "bone",
                "Bone Mass",
                "%",
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "waistline",
                "Waistline",
                "cm",
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "hip",
                "Hip",
                "cm",
                category="Measurements",
                label="Physical Metrics",
            ),
            RenphoSensor(
                renpho,
                "stature",
                "Stature",
                "cm",
                category="Measurements",
                label="Physical Metrics",
            ),
            # Measurements - Body Composition
            RenphoSensor(
                renpho,
                "bodyfat",
                "Body Fat",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "water",
                "Water Content",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "subfat",
                "Subcutaneous Fat",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "visfat",
                "Visceral Fat",
                "Level",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "bodyfat_left_arm",
                "Body Fat Left Arm",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "bodyfat_right_arm",
                "Body Fat Right Arm",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "bodyfat_left_leg",
                "Body Fat Left Leg",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "bodyfat_right_leg",
                "Body Fat Right Leg",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            RenphoSensor(
                renpho,
                "bodyfat_trunk",
                "Body Fat Trunk",
                "%",
                category="Measurements",
                label="Body Composition",
            ),
            # Measurements - Metabolic Metrics
            RenphoSensor(
                renpho,
                "bmr",
                "BMR",
                "kcal/day",
                category="Measurements",
                label="Metabolic Metrics",
            ),
            RenphoSensor(
                renpho,
                "protein",
                "Protein Content",
                "%",
                category="Measurements",
                label="Metabolic Metrics",
            ),
            # Measurements - Age Metrics
            RenphoSensor(
                renpho,
                "bodyage",
                "Body Age",
                "Years",
                category="Measurements",
                label="Age Metrics",
            ),
            # Device Information
            RenphoSensor(
                renpho,
                "mac",
                "MAC Address",
                "",
                category="Device",
                label="Device Information",
            ),
            RenphoSensor(
                renpho,
                "scale_type",
                "Scale Type",
                "",
                category="Device",
                label="Device Information",
            ),
            RenphoSensor(
                renpho,
                "scale_name",
                "Scale Name",
                "",
                category="Device",
                label="Device Information",
            ),
            RenphoSensor(
                renpho,
                "internal_model",
                "Internal Model",
                "",
                category="Device",
                label="Device Information",
            ),
            RenphoSensor(
                renpho,
                "time_zone",
                "Time Zone",
                "",
                category="Device",
                label="Device Information",
            ),
            # Miscellaneous
            RenphoSensor(
                renpho,
                "method",
                "Measurement Method",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "pregnant_flag",
                "Pregnant Flag",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "sport_flag",
                "Sport Flag",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "score",
                "Score",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "remark",
                "Remark",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "category",
                "Category",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "category_type",
                "Category Type",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "person_type",
                "Person Type",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "height_unit",
                "Height Unit",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
            RenphoSensor(
                renpho,
                "weight_unit",
                "Weight Unit",
                "",
                category="Miscellaneous",
                label="Additional Metrics",
            ),
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

    def update(self) -> None:
        """ Update the sensor. """
        try:
            self._state = self._renpho.getSpecificMetric(self._metric)
            self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            _LOGGER.error(f"Error updating {self._name} sensor: {e}")
