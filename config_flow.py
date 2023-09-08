from __future__ import annotations
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_USER_ID, CONF_PUBLIC_KEY, CONF_EMAIL, CONF_PASSWORD
from .RenphoWeight import RenphoWeight

_LOGGER = logging.getLogger(__name__)

# Define the data schema with suggested values for better user experience
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL, description={"suggested_value": "example@email.com"}): str,
    vol.Required(CONF_PASSWORD, description={"suggested_value": "YourPasswordHere"}): str,
    vol.Optional(CONF_USER_ID, description={"suggested_value": "OptionalUserID"}): str,
})

async def async_validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    _LOGGER.debug("Starting to validate input: %s", data)
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
        _LOGGER.debug("Handling user step. Input received: %s", user_input)
        
        errors = {}
        if user_input is not None:
            try:
                _LOGGER.debug("Validating user input")
                info = await async_validate_input(self.hass, user_input)
                _LOGGER.debug("User input validated. Creating entry.")
                
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                _LOGGER.error("Cannot connect or invalid credentials")
                errors["base"] = "CannotConnect"
            except exceptions.HomeAssistantError as e:
                _LOGGER.error("Home Assistant specific error: %s", str(e))
                errors["base"] = "HomeAssistantError"
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception: %s", e)
                errors["base"] = "UnknownError"
        
        _LOGGER.debug("Showing form with errors: %s", errors)
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
            description_placeholders={"additional_info": "Please provide your Renpho login details."},
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""