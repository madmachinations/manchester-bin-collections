#!/usr/bin/env python3

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensors from a config entry created in the integrations UI."""

    api = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        BinCollectionIsTomorrow(api),
        BinCollectionIsToday(api)
    ]

    async_add_entities(entities, update_before_add=True)


class BinCollectionIsTomorrow(BinarySensorEntity):
    """Check if the next bin collection is tomorrow"""

    def __init__(self, api):
        self.api = api

        self._attr_name = "Bin collection is tomorrow"
        self._attr_icon = "mdi:calendar-alert"
        self._attr_device_class = BinarySensorDeviceClass.MOTION
        self._attr_unique_id = api.street_address_id + "__" + "bin_collection_is_tomorrow"
    

    async def async_update(self) -> None:
        await self.api.update()

        if self.api.get_days_until_next_collection() == 1:
            self._attr_is_on = True
        else:
            self._attr_is_on = False


class BinCollectionIsToday(BinarySensorEntity):
    """Check if the next bin collection is today"""

    def __init__(self, api):
        self.api = api

        self._attr_name = "Bin collection is today"
        self._attr_icon = "mdi:calendar-alert"
        self._attr_device_class = BinarySensorDeviceClass.MOTION
        self._attr_unique_id = api.street_address_id + "__" + "bin_collection_is_today"
    

    async def async_update(self) -> None:
        await self.api.update()

        if self.api.get_days_until_next_collection() == 0:
            self._attr_is_on = True
        else:
            self._attr_is_on = False