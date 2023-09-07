# Constants for the Renpho integration

# The domain of the component. Used to store data in hass.data.
from typing import Final


DOMAIN: Final = "renpho"

EVENT_HOMEASSISTANT_CLOSE: Final = "homeassistant_close"
EVENT_HOMEASSISTANT_START: Final = "homeassistant_start"
EVENT_HOMEASSISTANT_STARTED: Final = "homeassistant_started"
EVENT_HOMEASSISTANT_STOP: Final = "homeassistant_stop"
MASS_KILOGRAMS: Final = "kg"
TIME_SECONDS: Final = "s"

# Configuration keys
CONF_EMAIL: Final = 'email'        # The email used for Renpho login
CONF_PASSWORD: Final = 'password'  # The password used for Renpho login
CONF_REFRESH: Final = 'refresh'    # Refresh rate for pulling new data
CONF_UNIT: Final = 'unit'          # Unit of measurement for weight (kg/lbs)
CONF_USER_ID: Final = 'user_id'    # The ID of the user for whom weight data should be fetched

KG_TO_LBS: Final = 2.20462
CM_TO_INCH: Final = 0.393701

# Public key for encrypting the password
CONF_PUBLIC_KEY: Final = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744
u2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm
Jr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ
IiOL2CUBzu+HmIfUbQIDAQAB
-----END PUBLIC KEY-----'''
