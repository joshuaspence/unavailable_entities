from datetime import timedelta
import logging
from typing import List, Optional
import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

from homeassistant.const import (
    CONF_EXCLUDE,
    CONF_FRIENDLY_NAME,
    CONF_UNIQUE_ID,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_NAME = "unavailable_entities"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
        vol.Optional(CONF_EXCLUDE, default=[]): vol.All(
            cv.ensure_list, [cv.entity_ids]
        ),
    }
)


async def async_setup_platform(
    hass: HomeAssistant, config, async_add_entities, discovery_info=None
):
    unique_id = config.get(CONF_UNIQUE_ID)
    friendly_name = config.get(CONF_FRIENDLY_NAME)
    exclude = config.get(CONF_EXCLUDE)

    hass.data[PLATFORM_NAME] = {}
    sensors = []

    sensors.append(UnavailableEntitiesSensor(hass, unique_id, friendly_name, exclude))

    async_add_entities(sensors, True)


class UnavailableEntitiesSensor(Entity):
    def __init__(
        self,
        hass: HomeAssistant,
        unique_id: Optional[str],
        friendly_name: Optional[str],
        exclude: List[str] = [],
    ) -> None:
        super().__init__()

        self.hass: HomeAssistant = hass
        self._attr_unique_id = unique_id
        self._attr_name = friendly_name
        self._exclude: List[str] = exclude

        self._state = 0

    @property
    def entity_id(self) -> str:
        return "sensor.unavailable_entities"

    @property
    def name(self) -> str:
        return "Unavailable entities"

    @property
    def icon(self):
        return "mdi:check-circle"

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return None
