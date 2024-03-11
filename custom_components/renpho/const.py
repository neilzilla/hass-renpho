# Constants for the Renpho integration

# The domain of the component. Used to store data in hass.data.
from typing import Final

DOMAIN: Final = "renpho"
VERSION: Final = "1.0.0"
EVENT_HOMEASSISTANT_CLOSE: Final = "homeassistant_close"
EVENT_HOMEASSISTANT_START: Final = "homeassistant_start"
EVENT_HOMEASSISTANT_STARTED: Final = "homeassistant_started"
EVENT_HOMEASSISTANT_STOP: Final = "homeassistant_stop"
MASS_KILOGRAMS: Final = "kg"
MASS_POUNDS: Final = "lbs"
TIME_SECONDS: Final = "s"


# Configuration keys
CONF_EMAIL: Final = "email"  # The email used for Renpho login
CONF_PASSWORD: Final = "password"  # The password used for Renpho login
CONF_REFRESH: Final = "refresh"  # Refresh rate for pulling new data
CONF_UNIT: Final = "unit"  # Unit of measurement for weight (kg/lbs)
CONF_USER_ID: Final = (
    "user_id"  # The ID of the user for whom weight data should be fetched
)
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"

KG_TO_LBS: Final = 2.2046226218
CM_TO_INCH: Final = 0.393701

# General Information Metrics
ID: Final = "id"
B_USER_ID: Final = "b_user_id"
TIME_STAMP: Final = "time_stamp"
CREATED_AT: Final = "created_at"
CREATED_STAMP: Final = "created_stamp"

# Device Information Metrics
SCALE_TYPE: Final = "scale_type"
SCALE_NAME: Final = "scale_name"
MAC: Final = "mac"
INTERNAL_MODEL: Final = "internal_model"
TIME_ZONE: Final = "time_zone"

# User Profile Metrics
GENDER: Final = "gender"
HEIGHT: Final = "height"
HEIGHT_UNIT: Final = "height_unit"
BIRTHDAY: Final = "birthday"

# Physical Metrics
WEIGHT: Final = "weight"
BMI: Final = "bmi"
MUSCLE: Final = "muscle"
BONE: Final = "bone"
WAISTLINE: Final = "waistline"
HIP: Final = "hip"
STATURE: Final = "stature"

# Body Composition Metrics
BODYFAT: Final = "bodyfat"
WATER: Final = "water"
SUBFAT: Final = "subfat"
VISFAT: Final = "visfat"

# Metabolic Metrics
BMR: Final = "bmr"
PROTEIN: Final = "protein"

# Age Metrics
BODYAGE: Final = "bodyage"

GIRTH_METRICS: Final = [
    "neck_value",
    "shoulder_value",
    "arm_value",
    "chest_value",
    "waist_value",
    "hip_value",
    "thigh_value",
    "calf_value",
    "left_arm_value",
    "left_thigh_value",
    "left_calf_value",
    "right_arm_value",
    "right_thigh_value",
    "right_calf_value",
    "whr_value",
    "abdomen_value",
    "custom",
    "custom_value",
    "custom_unit",
    "custom1",
    "custom_value1",
    "custom_unit1",
    "custom2",
    "custom_value2",
    "custom_unit2",
    "custom3",
    "custom_value3",
    "custom_unit3",
    "custom4",
    "custom_value4",
    "custom_unit4",
    "custom5",
    "custom_value5",
    "custom_unit5",
]

GIRTH_GOALS: Final = [
    "girth_type",
    "setup_goal_at",
    "goal_value",
    "goal_unit",
    "initial_value",
    "initial_unit",
    "finish_goal_at",
    "finish_value",
    "finish_unit",
]

METRIC_TYPE_WEIGHT: Final = "weight"
METRIC_TYPE_GROWTH_RECORD: Final = "growth_record"
METRIC_TYPE_GIRTH: Final = "girth"
METRIC_TYPE_GIRTH_GOAL: Final = "girth_goals"

METRIC_TYPE = [
    METRIC_TYPE_WEIGHT,
    METRIC_TYPE_GROWTH_RECORD,
    METRIC_TYPE_GIRTH,
    METRIC_TYPE_GIRTH_GOAL,
]

# Public key for encrypting the password
CONF_PUBLIC_KEY: Final = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744
u2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm
Jr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ
IiOL2CUBzu+HmIfUbQIDAQAB
-----END PUBLIC KEY-----"""
