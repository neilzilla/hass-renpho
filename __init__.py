"""Init Renpho sensor."""

import logging
import voluptuous as vol
from homeassistant import core
from homeassistant.helpers.discovery import async_load_platform
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD_HASH, CONF_REFRESH, CONF_WEIGHT_UNITS, DEFAULT_CONF_WEIGHT_UNITS, DEFAULT_CONF_REFRESH
from .RenphoWeight import RenphoWeight

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD_HASH): str,
                vol.Optional(
                    CONF_WEIGHT_UNITS, default=CONF_WEIGHT_UNITS
                ): str,
                vol.Optional(
                    CONF_REFRESH, default=DEFAULT_CONF_REFRESH
                ): vol.All(cv.time_period, cv.positive_timedelta),
            }
        )
    },
    # The full HA configurations gets passed to `async_setup` so we need to allow
    # extra keys.
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the platform.
    @NOTE: `config` is the full dict from `configuration.yaml`.
    :returns: A boolean to indicate that initialization was successful.
    """
    
    conf = config[DOMAIN]
    email = conf[CONF_EMAIL]
    password_hash = conf[CONF_PASSWORD_HASH]
    unit_of_measurements = conf[CONF_WEIGHT_UNITS]
    refresh_interval = conf[CONF_REFRESH]
    
    renpho = RenphoWeight(email, password_hash, async_get_clientsession(hass), unit_of_measurements)
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=renpho.async_getInfo,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=refresh_interval,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN] = {
        "conf": conf,
        "coordinator": coordinator,
    }
    
    hass.async_create_task(async_load_platform(hass, "sensor", DOMAIN, {}, conf))
    return True