import logging
import asyncio
from homeassistant.helpers import service
from homeassistant.core import callback

from .const import (
    CONF_USER_ID, DOMAIN, CONF_EMAIL, CONF_PASSWORD,
    CONF_REFRESH, CONF_PUBLIC_KEY,
    EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
)
from .RenphoWeight import RenphoWeight

# Initialize logger
_LOGGER = logging.getLogger(__name__)

# ------------------- Setup Methods -------------------

async def async_setup(hass, config):
    """Set up the Renpho component from YAML configuration."""
    _LOGGER.debug("Starting hass_renpho")
    
    conf = config.get(DOMAIN)
    if conf:
        await setup_renpho(hass, conf)
    return True

async def async_setup_entry(hass, entry):
    """Set up Renpho from a config entry."""
    await setup_renpho(hass, entry.data)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # Remove Renpho instance if it exists
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
        return True

# ------------------- Helper Methods -------------------

async def setup_renpho(hass, conf):
    """Common setup logic for YAML and UI."""
    email = conf[CONF_EMAIL]
    password = conf[CONF_PASSWORD]
    user_id = conf.get(CONF_USER_ID, None)
    refresh = conf.get(CONF_REFRESH, 600)
    
    renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)

    @callback
    def async_on_start(event):
        hass.async_create_task(async_prepare(hass, renpho, refresh))
    
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, async_on_start)
    hass.data[DOMAIN] = renpho

async def async_prepare(hass, renpho, refresh):
    """Prepare and start polling."""
    await renpho.startPolling(refresh)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_cleanup(renpho))

async def async_cleanup(renpho):
    """Cleanup logic."""
    await renpho.stopPolling()

# ------------------- Main Method for Testing -------------------

if __name__ == "__main__":
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
