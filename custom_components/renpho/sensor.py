"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MASS_KILOGRAMS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import slugify

from .const import CM_TO_INCH, DOMAIN, KG_TO_LBS
from .renpho import _LOGGER, RenphoWeight


async def sensors_list(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> list[RenphoSensor]:
    sensor_configurations = [
        # Physical Metrics
        {
            "id": "weight",
            "name": "Weight",
            "unit": "kg",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "bmi",
            "name": "BMI",
            "unit": "",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "muscle",
            "name": "Muscle Mass",
            "unit": "%",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "bone",
            "name": "Bone Mass",
            "unit": "%",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "waistline",
            "name": "Waistline",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "hip",
            "name": "Hip",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        {
            "id": "stature",
            "name": "Stature",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
        },
        # Body Composition
        {
            "id": "bodyfat",
            "name": "Body Fat",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
        },
        {
            "id": "water",
            "name": "Water Content",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
        },
        {
            "id": "subfat",
            "name": "Subcutaneous Fat",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
        },
        {
            "id": "visfat",
            "name": "Visceral Fat",
            "unit": "Level",
            "category": "Measurements",
            "label": "Body Composition",
        },
        # Metabolic Metrics
        {
            "id": "bmr",
            "name": "BMR",
            "unit": "kcal/day",
            "category": "Measurements",
            "label": "Metabolic Metrics",
        },
        {
            "id": "protein",
            "name": "Protein Content",
            "unit": "%",
            "category": "Measurements",
            "label": "Metabolic Metrics",
        },
        # Age Metrics
        {
            "id": "bodyage",
            "name": "Body Age",
            "unit": "Years",
            "category": "Measurements",
            "label": "Age Metrics",
        },
        # Device Information
        {
            "id": "mac",
            "name": "MAC Address",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
        },
        {
            "id": "scale_type",
            "name": "Scale Type",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
        },
        {
            "id": "scale_name",
            "name": "Scale Name",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
        },
        # Miscellaneous
        {
            "id": "method",
            "name": "Measurement Method",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
        },
        {
            "id": "pregnant_flag",
            "name": "Pregnant Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
        },
        {
            "id": "sport_flag",
            "name": "Sport Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
        },
        {
            "id": "score",
            "name": "Score",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
        },
        {
            "id": "remark",
            "name": "Remark",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
        },
        # Meta Information
        {
            "id": "id",
            "name": "Record ID",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
        },
        {
            "id": "b_user_id",
            "name": "User ID",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
        },
        {
            "id": "time_stamp",
            "name": "Time Stamp",
            "unit": "UNIX Time",
            "category": "Meta",
            "label": "Meta Information",
        },
        {
            "id": "created_at",
            "name": "Created At",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
        },
        # User Profile
        {
            "id": "gender",
            "name": "Gender",
            "unit": "",
            "category": "User",
            "label": "User Profile",
        },
        {
            "id": "height",
            "name": "Height",
            "unit": "cm",
            "category": "User",
            "label": "User Profile",
        },
        {
            "id": "birthday",
            "name": "Birthday",
            "unit": "",
            "category": "User",
            "label": "User Profile",
        },
        # Electrical Measurements
        {
            "id": "resistance",
            "name": "Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "sec_resistance",
            "name": "Secondary Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "actual_resistance",
            "name": "Actual Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "actual_sec_resistance",
            "name": "Actual Secondary Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance20_left_arm",
            "name": "Resistance20 Left Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance20_left_leg",
            "name": "Resistance20 Left Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance20_right_arm",
            "name": "Resistance20 Right Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance20_right_leg",
            "name": "Resistance20 Right Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance20_trunk",
            "name": "Resistance20 Trunk",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance100_left_arm",
            "name": "Resistance100 Left Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance100_left_leg",
            "name": "Resistance100 Left Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance100_right_arm",
            "name": "Resistance100 Right Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance100_right_leg",
            "name": "Resistance100 Right Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        {
            "id": "resistance100_trunk",
            "name": "Resistance100 Trunk",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
        },
        # Cardiovascular Metrics
        {
            "id": "heart_rate",
            "name": "Heart Rate",
            "unit": "bpm",
            "category": "Measurements",
            "label": "Cardiovascular Metrics",
        },
        {
            "id": "cardiac_index",
            "name": "Cardiac Index",
            "unit": "",
            "category": "Measurements",
            "label": "Cardiovascular Metrics",
        },
        # Other Metrics
        {
            "id": "method",
            "name": "Method Used",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        {
            "id": "sport_flag",
            "name": "Sports Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        {
            "id": "left_weight",
            "name": "Left Weight",
            "unit": "kg",
            "category": "Measurements",
            "label": "Other Metrics",
        },
        {
            "id": "right_weight",
            "name": "Right Weight",
            "unit": "kg",
            "category": "Measurements",
            "label": "Other Metrics",
        },
        {
            "id": "local_created_at",
            "name": "Local Created At",
            "unit": "",
            "category": "Meta",
            "label": "Other Metrics",
        },
        {
            "id": "time_zone",
            "name": "Time Zone",
            "unit": "",
            "category": "Device",
            "label": "Other Metrics",
        },
        {
            "id": "remark",
            "name": "Additional Remarks",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        {
            "id": "score",
            "name": "Health Score",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        {
            "id": "pregnant_flag",
            "name": "Pregnancy Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        {
            "id": "stature",
            "name": "Stature Information",
            "unit": "cm",
            "category": "Measurements",
            "label": "Other Metrics",
        },
        {
            "id": "category",
            "name": "Category Identifier",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
        },
        # Girth Measurements
        {
            "id": "neck_value",
            "name": "Neck Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "shoulder_value",
            "name": "Shoulder Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "arm_value",
            "name": "Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "chest_value",
            "name": "Chest Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "waist_value",
            "name": "Waist Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "hip_value",
            "name": "Hip Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "thigh_value",
            "name": "Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "calf_value",
            "name": "Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "left_arm_value",
            "name": "Left Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "left_thigh_value",
            "name": "Left Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "left_calf_value",
            "name": "Left Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "right_arm_value",
            "name": "Right Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "right_thigh_value",
            "name": "Right Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "right_calf_value",
            "name": "Right Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "whr_value",
            "name": "WHR Value",
            "unit": "ratio",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        {
            "id": "abdomen_value",
            "name": "Abdomen Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
        },
        # Girth Goals
        {
            "id": "neck_goal_value",
            "name": "Neck Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "shoulder_goal_value",
            "name": "Shoulder Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "arm_goal_value",
            "name": "Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "chest_goal_value",
            "name": "Chest Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "waist_goal_value",
            "name": "Waist Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "hip_goal_value",
            "name": "Hip Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "thigh_goal_value",
            "name": "Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "calf_goal_value",
            "name": "Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "left_arm_goal_value",
            "name": "Left Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "left_thigh_goal_value",
            "name": "Left Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "left_calf_goal_value",
            "name": "Left Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "right_arm_goal_value",
            "name": "Right Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "right_thigh_goal_value",
            "name": "Right Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "right_calf_goal_value",
            "name": "Right Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "whr_goal_value",
            "name": "WHR Goal Value",
            "unit": "ratio",
            "category": "Goals",
            "label": "Girth Goals",
        },
        {
            "id": "abdomen_goal_value",
            "name": "Abdomen Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
        },
    ]

    return [
        RenphoSensor(hass.data[DOMAIN], **config) for config in sensor_configurations
    ]


async def async_setup(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    sensor_entities = await sensors_list(hass, config_entry)
    async_add_entities(sensor_entities)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
):
    sensor_entities = sensors_list(hass, discovery_info)
    add_entities(sensor_entities)


class RenphoSensor(SensorEntity):
    def __init__(
        self,
        renpho: RenphoWeight,
        metric: str,
        name: str,
        unit_of_measurement: str,
        category="Renpho",
        label="Data",
        convert_unit=False,
    ) -> None:
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
            "timestamp": self._timestamp,
            "category": self._category,
            "label": self._label,
        }

    def convert_unit(self, value, unit):
        conversions = {"kg": value * KG_TO_LBS, "cm": value * CM_TO_INCH}
        return conversions.get(unit, value)

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        """Return the state of the sensor.
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
        """Return the unit of measurement.
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
        """Return the category of the sensor."""
        return self._category

    @property
    def label(self) -> str:
        """Return the label of the sensor."""
        return self._label


async def async_update(self):
    """Update the sensor using the event loop for asynchronous code."""
    try:
        metric_value = await self._renpho.get_specific_metric(self._metric)

        # Update state with the new metric_value
        self._state = metric_value if metric_value is not None else self._state

        # Convert the unit if necessary
        self._state = self.convert_unit(self._state, self._unit_of_measurement)

        # Update the timestamp
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        _LOGGER.info(f"Successfully updated {self._name}")
    except (ConnectionError, TimeoutError) as e:
        _LOGGER.error(f"{type(e).__name__} updating {self._name}: {e}")
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred updating {self._name}: {e}")
