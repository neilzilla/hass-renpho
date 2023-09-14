"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MASS_KILOGRAMS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import slugify

from .const import CM_TO_INCH, DOMAIN, KG_TO_LBS, METRIC_TYPE, METRIC_TYPE_WEIGHT, METRIC_TYPE_GIRTH, METRIC_TYPE_GIRTH_GOAL
from .api_renpho import _LOGGER, RenphoWeight


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
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "bmi",
            "name": "BMI",
            "unit": "",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "muscle",
            "name": "Muscle Mass",
            "unit": "%",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "bone",
            "name": "Bone Mass",
            "unit": "%",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "waistline",
            "name": "Waistline",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "hip",
            "name": "Hip",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "stature",
            "name": "Stature",
            "unit": "cm",
            "category": "Measurements",
            "label": "Physical Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Body Composition
        {
            "id": "bodyfat",
            "name": "Body Fat",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "water",
            "name": "Water Content",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "subfat",
            "name": "Subcutaneous Fat",
            "unit": "%",
            "category": "Measurements",
            "label": "Body Composition",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "visfat",
            "name": "Visceral Fat",
            "unit": "Level",
            "category": "Measurements",
            "label": "Body Composition",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Metabolic Metrics
        {
            "id": "bmr",
            "name": "BMR",
            "unit": "kcal/day",
            "category": "Measurements",
            "label": "Metabolic Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "protein",
            "name": "Protein Content",
            "unit": "%",
            "category": "Measurements",
            "label": "Metabolic Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Age Metrics
        {
            "id": "bodyage",
            "name": "Body Age",
            "unit": "Years",
            "category": "Measurements",
            "label": "Age Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Device Information
        {
            "id": "mac",
            "name": "MAC Address",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "scale_type",
            "name": "Scale Type",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "scale_name",
            "name": "Scale Name",
            "unit": "",
            "category": "Device",
            "label": "Device Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Miscellaneous
        {
            "id": "method",
            "name": "Measurement Method",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "pregnant_flag",
            "name": "Pregnant Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "sport_flag",
            "name": "Sport Flag",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "score",
            "name": "Score",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "remark",
            "name": "Remark",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Additional Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Meta Information
        {
            "id": "id",
            "name": "Record ID",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "b_user_id",
            "name": "User ID",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "time_stamp",
            "name": "Time Stamp",
            "unit": "UNIX Time",
            "category": "Meta",
            "label": "Meta Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "created_at",
            "name": "Created At",
            "unit": "",
            "category": "Meta",
            "label": "Meta Information",
            "metric": METRIC_TYPE_WEIGHT
        },
        # User Profile
        {
            "id": "gender",
            "name": "Gender",
            "unit": "",
            "category": "User",
            "label": "User Profile",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "height",
            "name": "Height",
            "unit": "cm",
            "category": "User",
            "label": "User Profile",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "birthday",
            "name": "Birthday",
            "unit": "",
            "category": "User",
            "label": "User Profile",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Electrical Measurements
        {
            "id": "resistance",
            "name": "Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "sec_resistance",
            "name": "Secondary Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "actual_resistance",
            "name": "Actual Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "actual_sec_resistance",
            "name": "Actual Secondary Electrical Resistance",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance20_left_arm",
            "name": "Resistance20 Left Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance20_left_leg",
            "name": "Resistance20 Left Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance20_right_arm",
            "name": "Resistance20 Right Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance20_right_leg",
            "name": "Resistance20 Right Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance20_trunk",
            "name": "Resistance20 Trunk",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance100_left_arm",
            "name": "Resistance100 Left Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance100_left_leg",
            "name": "Resistance100 Left Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance100_right_arm",
            "name": "Resistance100 Right Arm",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance100_right_leg",
            "name": "Resistance100 Right Leg",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "resistance100_trunk",
            "name": "Resistance100 Trunk",
            "unit": "Ohms",
            "category": "Measurements",
            "label": "Electrical Measurements",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Cardiovascular Metrics
        {
            "id": "heart_rate",
            "name": "Heart Rate",
            "unit": "bpm",
            "category": "Measurements",
            "label": "Cardiovascular Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "cardiac_index",
            "name": "Cardiac Index",
            "unit": "",
            "category": "Measurements",
            "label": "Cardiovascular Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Other Metrics
        {
            "id": "method",
            "name": "Method Used",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "left_weight",
            "name": "Left Weight",
            "unit": "kg",
            "category": "Measurements",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "right_weight",
            "name": "Right Weight",
            "unit": "kg",
            "category": "Measurements",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "local_created_at",
            "name": "Local Created At",
            "unit": "",
            "category": "Meta",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "remark",
            "name": "Additional Remarks",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "stature",
            "name": "Stature Information",
            "unit": "cm",
            "category": "Measurements",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        {
            "id": "category",
            "name": "Category Identifier",
            "unit": "",
            "category": "Miscellaneous",
            "label": "Other Metrics",
            "metric": METRIC_TYPE_WEIGHT
        },
        # Girth Measurements
        {
            "id": "neck_value",
            "name": "Neck Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "shoulder_value",
            "name": "Shoulder Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_arm_value",
            "name": "Left Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_arm_value",
            "name": "Right Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "chest_value",
            "name": "Chest Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "waist_value",
            "name": "Waist Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "hip_value",
            "name": "Hip Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_thigh_value",
            "name": "Left Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_thigh_value",
            "name": "Right Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_calf_value",
            "name": "Left Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_calf_value",
            "name": "Right Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_arm_value",
            "name": "Left Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_thigh_value",
            "name": "Left Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "left_calf_value",
            "name": "Left Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_arm_value",
            "name": "Right Arm Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_thigh_value",
            "name": "Right Thigh Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "right_calf_value",
            "name": "Right Calf Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "whr_value",
            "name": "WHR Value",
            "unit": "ratio",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        {
            "id": "abdomen_value",
            "name": "Abdomen Value",
            "unit": "cm",
            "category": "Measurements",
            "label": "Girth Measurements",
            "metric": METRIC_TYPE_GIRTH
        },
        # Girth Goals
        {
            "id": "neck",
            "name": "Neck Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "shoulder",
            "name": "Shoulder Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "arm",
            "name": "Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "chest",
            "name": "Chest Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "waist",
            "name": "Waist Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "hip",
            "name": "Hip Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "thigh",
            "name": "Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "calf",
            "name": "Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "left_arm",
            "name": "Left Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "left_thigh",
            "name": "Left Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "left_calf",
            "name": "Left Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "right_arm",
            "name": "Right Arm Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "right_thigh",
            "name": "Right Thigh Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "right_calf",
            "name": "Right Calf Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "whr",
            "name": "WHR Goal Value",
            "unit": "ratio",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
        },
        {
            "id": "abdomen",
            "name": "Abdomen Goal Value",
            "unit": "cm",
            "category": "Goals",
            "label": "Girth Goals",
            "metric": METRIC_TYPE_GIRTH_GOAL
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

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensor platform."""
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
        id: str,
        name: str,
        unit: str,
        category: str,
        label: str,
        metric: str,
        convert_unit=False,
    ) -> None:
        self._renpho = renpho
        self._metric = metric
        self._id = id
        self._name = f"Renpho {name}"
        self._unit = unit
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

    def convert_unit(self, value: Optional[float], unit: str) -> Optional[float]:
        """Convert unit based on the conversion mapping."""
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
            if self._unit == MASS_KILOGRAMS:
                return self.kg_to_lbs(self._state)
            elif self._unit == "cm":
                return self.cm_to_inch(self._state)
        return self._state

    @property
    def unit(self) -> str:
        """Return the unit of measurement.
        If the unit is kg or cm, convert to lbs or inch respectively.

        """
        if self._convert_unit:
            if self._unit == MASS_KILOGRAMS:
                return "lbs"
            elif self._unit == "cm":
                return "inch"
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
        """Update the sensor using the event loop for asynchronous code."""
        try:
            metric_value = await self._renpho.get_specific_metric(
                metric_type=self._metric,
                metric=self._id,
                user_id=None
            )

            if metric_value is not None:
                self._state = metric_value

                # Convert the unit if necessary
                # if self._unit is not None or self._unit != "":
                #     self._state = self.convert_unit(self._state, self._unit)

                # Update the timestamp
                self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                _LOGGER.info(f"Successfully updated {self._name} for metric type {self._metric}")

        except (ConnectionError, TimeoutError) as e:
            _LOGGER.error(f"{type(e).__name__} occurred while updating {self._name} for metric type {self._metric}: {e}")

        except Exception as e:
            _LOGGER.critical(f"An unexpected error occurred while updating {self._name} for metric type {self._metric}: {e}")