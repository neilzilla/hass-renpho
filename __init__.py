import logging

import voluptuous as vol

from homeassistant import core
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_COUNTRY, CONF_WISHLIST, DEFAULT_SCAN_INTERVAL, DOMAIN
from .eshop import Country, EShop

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_WISHLIST): cv.ensure_list,
                vol.Required(CONF_COUNTRY): cv.enum(Country),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
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
    country = conf[CONF_COUNTRY].name
    wishlist = conf[CONF_WISHLIST]
    scan_interval = conf[CONF_SCAN_INTERVAL]
    eshop = EShop(country, async_get_clientsession(hass), wishlist)
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=eshop.fetch_on_sale,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=scan_interval,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN] = {
        "conf": conf,
        "coordinator": coordinator,
    }
    hass.async_create_task(async_load_platform(hass, "sensor", DOMAIN, {}, conf))
    hass.async_create_task(async_load_platform(hass, "binary_sensor", DOMAIN, {}, conf))
    return True