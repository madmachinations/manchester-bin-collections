#!/usr/bin/env python3

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensors from a config entry created in the integrations UI."""

    api = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        BinNextCollectionDateSensor(api),
        NextBinsSensor(api),
        BinNextCollectionDayCountSensor(api)
    ]

    for bin in api.get_bin_keys():
        entities.append(BinCollectionDateSensor(api, bin))

    async_add_entities(entities, update_before_add=True)



class BinCollectionDateSensor(SensorEntity):
    """Date a specific bin will next be collected"""

    def __init__(self, api, bin_key):
        self.api = api
        self.bin_key = bin_key

        self._attr_name = api.get_bin_name(self.bin_key)
        self._attr_device_class = SensorDeviceClass.DATE
        self._attr_icon = "mdi:trash-can-outline"
        self._attr_unique_id = api.get_bin_unique_id(self.bin_key) + "__" + "next_date"
    

    async def async_update(self) -> None:
        await self.api.update()
        self._attr_native_value = self.api.get_bin_collection_date(self.bin_key)


class BinNextCollectionDateSensor(SensorEntity):
    """Date the next collection takes place"""

    def __init__(self, api):
        self.api = api

        self._attr_name = "Next bin collection"
        self._attr_device_class = SensorDeviceClass.DATE
        self._attr_icon = "mdi:calendar"
        self._attr_unique_id = api.street_address_id + "__" + "next_bin_collection_date"
    

    async def async_update(self) -> None:
        await self.api.update()
        self._attr_native_value = self.api.get_next_collection_date()


class BinNextCollectionDayCountSensor(SensorEntity):
    """Days until the next collection takes place"""

    def __init__(self, api):
        self.api = api

        self._attr_name = "Days until next bin collection"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_unique_id = api.street_address_id + "__" + "days_until_next_bin_collection"
    

    async def async_update(self) -> None:
        await self.api.update()
        self._attr_native_value = int(self.api.get_days_until_next_collection())


class NextBinsSensor(SensorEntity):
    """List of the next bins to be collected"""

    def __init__(self, api):
        self.api = api

        self._attr_name = "Next bins"
        self._attr_icon = "mdi:trash-can-outline"
        self._attr_unique_id = api.street_address_id + "__" + "next_bins"
    

    async def async_update(self) -> None:
        await self.api.update()
        bins = self.api.get_next_collected_bin_keys()

        collection_str = ""
        collection_count = 0

        for bin_key in bins:

            if collection_count > 0:
                if (collection_count + 1) == len(bins):
                    collection_str = collection_str + " and "
                else:
                    collection_str = collection_str + ", "

            collection_str = collection_str + self.api.get_bin_name(bin_key).replace(" Bin", "")
            collection_count = collection_count + 1

            if collection_count == len(bins):
                collection_str = collection_str + " Bin"
                if collection_count > 1:
                    collection_str = collection_str + "s"

        self._attr_native_value = collection_str
