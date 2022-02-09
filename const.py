from datetime import timedelta

"""Constants for constants sake"""

DOMAIN = "renpho_weight"

CONF_EMAIL = 'email'
CONF_PASSWORD_HASH = 'password_hash'
CONF_REFRESH = 'refresh'
CONF_WEIGHT_UNITS = 'weight_units'

DEFAULT_CONF_WEIGHT_UNITS = 'kg'
DEFAULT_CONF_REFRESH = timedelta(hours=3)

KG_TO_LB_MULTIPLICATOR = 2.2046226218