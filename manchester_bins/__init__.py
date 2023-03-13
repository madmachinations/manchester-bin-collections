#!/usr/bin/env python3

import logging
from .manchester import ManchesterBinCollectionApi

_LOGGER = logging.getLogger(__name__)

DOMAIN = "manchester_bins"
CONF_ADDRESS_ID = "address_id"


async def async_setup_entry(hass, entry):
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    api = ManchesterBinCollectionApi(entry.data[CONF_ADDRESS_ID])
    await api.connect()

    if api.failed == False:

        hass.data[DOMAIN][entry.entry_id] = api

        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "sensor")
        )

        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
        )

        return True
    
    else:
        return False