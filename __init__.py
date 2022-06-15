"""Init Renpho sensor."""
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_REFRESH, CONF_PUBLIC_KEY
from .RenphoWeight import RenphoWeight
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
import logging

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):

  _LOGGER.debug("Starting hass-renpho")

  conf = config[DOMAIN]
  email = conf[CONF_EMAIL]
  password = conf[CONF_PASSWORD]
  refresh = conf[CONF_REFRESH]

  renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password)

  def cleanup(event):
    renpho.stopPolling()

  def prepare(event):
    renpho.startPolling(refresh)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

  hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)
  hass.data[DOMAIN] = renpho

  return True