from datetime import datetime, timedelta
import logging

import async_timeout
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_UNIT_OF_MEASUREMENT

_LOGGER = logging.getLogger(__name__)

def create_coordinator(hass, config, api):
    """Create the data update coordinator."""
    return RenphoWeightCoordinator(hass, api=api, config=config)


class RenphoWeightCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, api, config):
        """Initialize."""
        self.api = api
        self.config = config
        self.hass = hass
        self._unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT, "kg")
        self._user_id = config.get("user_id", None)
        self._refresh = config.get("refresh", 60)
        self._unit = config.get("unit", "kg")
        self._email = config.get("email", None)
        self._password = config.get("password", None)
        self._data = {}
        self._last_updated = None

        self.api.auth()

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=self._refresh)
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            with async_timeout.timeout(10):
                await self.api.poll_data()
                self._last_updated = datetime.now()
        except Exception as e:
            _LOGGER.error(f"Error fetching data from Renpho API: {e}")
            raise UpdateFailed(f"Error fetching data: {e}") from e
    @property
    def last_updated(self):
        return self._last_updated

    async def get_specific_metric(self, metric_type: str, metric: str):
        return await self.api.get_specific_metric(metric_type = metric_type, metric = metric, user_id = self._user_id)
