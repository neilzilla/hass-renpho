from datetime import datetime, timedelta
import logging

import async_timeout
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

import asyncio

from .const import CONF_EMAIL, CONF_REFRESH, CONF_USER_ID, DOMAIN, CONF_UNIT_OF_MEASUREMENT

_LOGGER = logging.getLogger(__name__)

def create_coordinator(hass, api, config):
    """Create the data update coordinator."""
    return RenphoWeightCoordinator(hass=hass, api=api, config=config)


class RenphoWeightCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, api, config):
        """Initialize."""
        self.api = api
        self.config = config
        self.hass = hass
        self._unit_of_measurement = hass.data[CONF_UNIT_OF_MEASUREMENT]
        self._user_id = hass.data[CONF_USER_ID]
        self._refresh = hass.data[CONF_REFRESH]
        self._email = hass.data[CONF_EMAIL]
        self._data = {}
        self._last_updated = None

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=self._refresh)
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            with async_timeout.timeout(self._refresh):
                await self.api.get_info()
                await asyncio.sleep(5)
                await self.api.list_girth()
                await asyncio.sleep(5)
                await self.api.list_girth_goal()
                await asyncio.sleep(5)
            self._last_updated = datetime.now()
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout error fetching data from Renpho API.")
            raise UpdateFailed("Timeout error occurred while fetching data.")
        except asyncio.CancelledError:
            _LOGGER.error("Task was cancelled, possibly during shutdown.")
            # Don't raise UpdateFailed for CancelledError as it's a normal part of operation
        except Exception as e:
            _LOGGER.error(f"Error fetching data from Renpho API: {e}")
            raise UpdateFailed(f"Error fetching data: {e}") from e

    @property
    def last_updated(self):
        return self._last_updated
