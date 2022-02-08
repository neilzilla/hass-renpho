"""Init Renpho sensor."""
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD_HASH, CONF_REFRESH, CONF_WEIGHT_UNITS
from .RenphoWeight import RenphoWeight
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

def setup(hass, config):

  conf = config[DOMAIN]
  email = conf[CONF_EMAIL]
  password_hash = conf[CONF_PASSWORD_HASH]
  unit_of_measurements = conf[CONF_WEIGHT_UNITS]
  refresh = conf[CONF_REFRESH]

  renpho = RenphoWeight(email, password_hash, unit_of_measurements)

  def cleanup(event):
    renpho.stopPolling()

  def prepare(event):
    renpho.startPolling(refresh)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

  hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)
  hass.data[DOMAIN] = renpho

  return True