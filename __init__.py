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

async def async_setup(hass, config):
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
    async def async_cleanup(event):
        await renpho.stopPolling()

    # Define a prepare function
    async def async_prepare(event):
        await renpho.startPolling(refresh)
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_cleanup)

    # Register the prepare function
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, async_prepare)

    # Store the Renpho instance
    hass.data[DOMAIN] = renpho

    return True

if __name__ == "__main__":
    import asyncio

    async def main():
        renpho = RenphoWeight(CONF_PUBLIC_KEY, '<username>', '<password>', '<user_id>')
        await renpho.startPolling(10)
        print(await renpho.getScaleUsers())
        print(await renpho.getSpecificMetricFromUserID("bodyfat"))
        print(await renpho.getSpecificMetricFromUserID("bodyfat", "<user_id>"))
        print(await renpho.getInfo())
        input("Press Enter to stop polling")
        await renpho.stopPolling()

    asyncio.run(main())
