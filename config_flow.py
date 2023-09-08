from __future__ import annotations
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_USER_ID, CONF_PUBLIC_KEY, CONF_EMAIL, CONF_PASSWORD
from .RenphoWeight import RenphoWeight

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_USER_ID): str,
})

async def async_validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    renpho = RenphoWeight(data[CONF_EMAIL], data[CONF_PASSWORD], data.get(CONF_USER_ID, None))
    is_valid = await renpho.validate_credentials()
    if not is_valid:
        raise CannotConnect
    return {"title": data[CONF_EMAIL]}

class RenphoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        errors = {}
        if user_input is not None:
            try:
                info = await async_validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "Invalid credentials or cannot connect to Renpho."
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception: %s", e)
                errors["base"] = "An unknown error occurred."
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""