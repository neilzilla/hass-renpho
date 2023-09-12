import asyncio
import logging

from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_PUBLIC_KEY,
    CONF_REFRESH,
    CONF_USER_ID,
    DOMAIN,
    EVENT_HOMEASSISTANT_STOP,
)
from .api_renpho import RenphoWeight


# Initialize logger
_LOGGER = logging.getLogger(__name__)

# ------------------- Setup Methods -------------------


async def async_setup(hass, config):
    """Set up the Renpho component from YAML configuration."""
    _LOGGER.debug("Starting hass_renpho")

    if conf := config.get(DOMAIN):
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
    renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id, refresh)

    # @callback
    # def async_on_start(event):
    #     hass.async_create_task(async_prepare(hass, renpho, refresh))

    # hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, async_on_start)
    hass.data[DOMAIN] = renpho


async def async_prepare(hass, renpho, refresh):
    """Prepare and start polling."""
    await renpho.start_polling(refresh)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_cleanup(renpho))


async def async_cleanup(renpho):
    """Cleanup logic."""
    await renpho.stop_polling()


# ------------------- Main Method for Testing -------------------

if __name__ == "__main__":

    async def main():
        import os

        from dotenv import load_dotenv

        load_dotenv()
        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        user_id = os.environ.get("USER_ID", None)
        try:
            renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)
            print("Before polling")
            renpho.start_polling(10)
            print("After polling")
            renpho.get_info_sync()
            users = await renpho.get_scale_users()
            print("Fetched scale users:", users)
            get_device_info = await renpho.get_device_info()
            print("Fetched device info:", get_device_info)
            list_growth_record = await renpho.list_growth_record()
            print("Fetched list growth record:", list_growth_record)
            list_girth = await renpho.list_girth()
            print("Fetched list girth:", list_girth)
            list_girth_goal = await renpho.list_girth_goal()
            print("Fetched list girth goal:", list_girth_goal)
            message_list = await renpho.message_list()
            list_growth_record = await renpho.list_growth_record()
            print("Fetched list growth record:", list_growth_record)
            print("Fetched message list:", message_list)
            info = await renpho.get_info()
            print("Fetched info:", info)
        except Exception as e:
            print(f"An exception occurred: {e}")

        input("Press Enter to stop polling")
        renpho.stop_polling()

    asyncio.run(main())
