from datetime import timedelta
import logging
from typing import List, Optional

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_EXCLUDE, CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_EXCLUDE, default=[]): vol.All(
            cv.ensure_list, [cv.entity_ids]
        ),
    }
)


def setup_platform(
    hass: HomeAssistant, config, add_entities, discovery_info=None
):
    unique_id = config.get(CONF_UNIQUE_ID)
    name = config.get(CONF_NAME)
    exclude = config.get(CONF_EXCLUDE)

    add_entities(
        [
            UnavailableEntitiesSensor(
                unique_id,
                name,
                exclude,
            )
        ],
        True)

    return True


class UnavailableEntitiesSensor(Entity):
    def __init__(
        self,
        unique_id: Optional[str],
        name: Optional[str],
        exclude: List[str] = [],
    ) -> None:
        self._unique_id = unique_id
        self._name = name
        self._exclude = exclude

    @property
    def device_class(self) -> Optional[str]:
        return super().device_class

    @property
    def entity_id(self) -> Optional[str]:
        return "sensor.unavailable_entities"

    @property
    def extra_state_attributes(self):
        return {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def should_poll(self) -> bool:
        # TODO: Stop using polling.
        return True

    @property
    def state(self):
        return self._state

    @property
    def state_class(self) -> Optional[str]:
        return super().state_class

    @property
    def unique_id(self) -> Optional[str]:
        return self._unique_id

    @property
    def unit_of_measurement(self) -> Optional[str]:
        return None

    def update(self):
        self._state = 0


    #@property
    #def icon(self):
    #    return "mdi:check-circle"

    #@property
    #def device_state_attributes(self):
    #    return None
