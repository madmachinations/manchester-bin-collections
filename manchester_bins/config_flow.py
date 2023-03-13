"""Config flow to configure Manchester bins."""
from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaFlowFormStep,
    SchemaOptionsFlowHandler,
)

from . import DOMAIN, CONF_ADDRESS_ID
from .manchester import get_street_address_options

_LOGGER = logging.getLogger(__name__)


class ManchesterBinsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle manchester bins config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the flow."""
        self.post_code = None
        self.address_id = None


    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""

        errors = {}
        if user_input is not None:
            if len(await get_street_address_options(user_input["post_code"])) > 0:
                self.post_code = user_input["post_code"]
                return await self.async_step_address()
            else:
                errors["base"] = "invalid_postcode"

        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("post_code"): cv.string
        }), errors=errors)


    async def async_step_address(self, user_input=None):
        """Invoked when a user needs to pick their street address."""

        errors = {}
        if user_input is not None:
            self.address_id = user_input["address_id"]
            return self.async_create_entry(title="Manchester Bins", data={
                CONF_ADDRESS_ID: self.address_id
            })

        data_schema = {}

        options = []
        for address in await get_street_address_options(self.post_code):
            options.append({
                "value": address['id'],
                "label": address['address']
            })

        data_schema["address_id"] = selector.selector({
            "select": {
                "options": options,
            }
        })

        return self.async_show_form(step_id="address", data_schema=vol.Schema(data_schema), errors=errors)