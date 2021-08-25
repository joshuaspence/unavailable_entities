from typing import Any, Dict, Optional, Set

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType, StateType
import voluptuous as vol

ATTR_ENTITIES = "entities"

DEFAULT_NAME = "Unavailable Entities"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    # pylint: disable=unused-argument
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> bool:
    name = config.get(CONF_NAME)
    unique_id = config.get(CONF_UNIQUE_ID)

    add_entities(
        [UnavailableEntitiesSensor(hass, name, unique_id)],
        update_before_add=True,
    )

    return True


class UnavailableEntitiesSensor(Entity):
    def __init__(
        self,
        hass: HomeAssistant,
        name: Optional[str] = None,
        unique_id: Optional[str] = None,
    ) -> None:
        self.hass = hass
        self._name = name
        self._unique_id = unique_id
        self._state: Set[str] = set()

    @property
    def entity_id(self) -> str:
        return "sensor.unavailable_entities"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return {ATTR_ENTITIES: self._state}

    @property
    def icon(self) -> str:
        if self.state > 0:
            return "mdi:alert-circle"

        return "mdi:check-circle"

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def should_poll(self) -> bool:
        # TODO: Stop using polling.
        return True

    @property
    def state(self) -> StateType:
        return len(self._state)

    @property
    def unique_id(self) -> Optional[str]:
        return self._unique_id

    def update(self) -> None:
        entities = set()

        for state in self.hass.states.all():
            if state.entity_id == self.entity_id:
                continue

            if state.state in ["unavailable", "unknown"]:
                entities.add(state.entity_id)

        self._state = entities
