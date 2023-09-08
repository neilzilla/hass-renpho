"""Initialization for the Renpho sensor component."""

# Import necessary modules and classes
from .const import CONF_USER_ID, DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_REFRESH, CONF_PUBLIC_KEY, EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP, EVENT_HOMEASSISTANT_CLOSE
from .RenphoWeight import RenphoWeight
from .config_flow import RenphoConfigFlow
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
logging.basicConfig(level=logging.DEBUG)

# Initialize logger
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """
    Set up the Renpho component.

    Args:
        hass (HomeAssistant): Home Assistant core object.
        config (dict): Configuration for the component.

    Returns:
        bool: True if initialization was successful, False otherwise.
    """

    _LOGGER.debug("Starting hass-renpho")

    # Extract configuration values
    conf = config[DOMAIN]
    email = conf[CONF_EMAIL]
    password = conf[CONF_PASSWORD]
    user_id = conf[CONF_USER_ID]
    refresh = conf[CONF_REFRESH]

    # Create an instance of RenphoWeight
    renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)

    # Define a cleanup function to stop polling when Home Assistant stops
    def cleanup(event):
        renpho.stopPolling()

    # Define a prepare function to start polling when Home Assistant starts
    def prepare(event):
        renpho.startPolling(refresh)
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

    # Register the prepare function to be called when Home Assistant starts
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)

    # Store the Renpho instance in Home Assistant's data dictionary
    hass.data[DOMAIN] = renpho

    return True  # Initialization was successful

if __name__ == "__main__":
    renpho = RenphoWeight(CONF_PUBLIC_KEY, '<username>', '<password>', '<user_id>')
    renpho.startPolling(10)
    print(renpho.getScaleUsers())
    print(renpho.getSpecificMetricFromUserID("bodyfat"))
    print(renpho.getSpecificMetricFromUserID("bodyfat", "<user_id>"))
    print(renpho.getInfo())
    input("Press Enter to stop polling")
    renpho.stopPolling()