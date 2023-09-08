from homeassistant.helpers import service
from .const import (
    CONF_USER_ID, DOMAIN, CONF_EMAIL, CONF_PASSWORD,
    CONF_REFRESH, CONF_PUBLIC_KEY,
    EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
)
from .RenphoWeight import RenphoWeight
import logging

# Initialize logger
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the Renpho component."""
    _LOGGER.debug("Starting hass_renpho")

    # Extract configuration values
    conf = config[DOMAIN]
    email = conf[CONF_EMAIL]
    password = conf[CONF_PASSWORD]
    user_id = conf.get(CONF_USER_ID)  # Using get in case it's optional
    refresh = conf[CONF_REFRESH]

    # Create an instance of RenphoWeight
    renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)

    # Define a cleanup function
    def cleanup(event):
        renpho.stopPolling()

    # Define a prepare function
    def prepare(event):
        renpho.startPolling(refresh)
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

    # Register the prepare function
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)

    # Store the Renpho instance
    hass.data[DOMAIN] = renpho

    # Reload configuration function
    def reload_config(call):
        """Reload the Renpho component."""
        # Unload the current configuration
        hass.helpers.entity_component.async_unload_entities(DOMAIN)

        # Load the new configuration
        setup(hass, config)

    # Register the reload service
    hass.services.register(DOMAIN, 'reload', reload_config)

    return True

if __name__ == "__main__":
    renpho = RenphoWeight(CONF_PUBLIC_KEY, '<username>', '<password>', '<user_id>')
    renpho.startPolling(10)
    print(renpho.getScaleUsers())
    print(renpho.getSpecificMetricFromUserID("bodyfat"))
    print(renpho.getSpecificMetricFromUserID("bodyfat", "<user_id>"))
    print(renpho.getInfo())
    input("Press Enter to stop polling")
    renpho.stopPolling()
