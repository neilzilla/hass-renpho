import voluptuous as vol
from homeassistant import config_entries, data_entry_flow

from const import DOMAIN, CONF_USER_ID, CONF_PUBLIC_KEY, CONF_EMAIL, CONF_PASSWORD
from RenphoWeight import RenphoWeight

class RenphoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            # Extract the user input
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            user_id = user_input[CONF_USER_ID]

            renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)
            is_valid = True  # Replace this with actual validation logic

            if is_valid:
                return self.async_create_entry(
                    title=email,  # Use the email as the title
                    data={
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,
                        CONF_USER_ID: user_id,
                    },
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.OPTIONAL(CONF_USER_ID): str,
            }),
            errors=errors,
        )
