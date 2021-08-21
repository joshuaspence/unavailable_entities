from typing import Optional

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import voluptuous as vol

DEFAULT_NAME = "Unavailable Entities"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> bool:
    name = config.get(CONF_NAME)

    add_entities(
        [UnavailableEntitiesSensor(hass, name)],
        update_before_add=True,
    )

    return True


class UnavailableEntitiesSensor(Entity):
    def __init__(self, hass: HomeAssistant, name: Optional[str] = None) -> None:
        self.hass = hass
        self._name = name
        self._state = None

    @property
    def entity_id(self) -> str:
        return "sensor.unavailable_entities"

    @property
    def icon(self) -> str:
        if self.state == 0:
            return "mdi:check-circle"
        else:
            return "mdi:alert-circle"

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def should_poll(self) -> bool:
        # TODO: Stop using polling.
        return True

    @property
    def state(self) -> Optional[int]:
        return self._state

    def update(self) -> None:
        count = 0

        for state in self.hass.states.all():
            if state.entity_id == self.entity_id:
                continue

            if state.state in ["unavailable", "unknown"]:
                count += 1

        self._state = count
