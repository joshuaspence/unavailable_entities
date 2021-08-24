from typing import Any, Dict

from homeassistant.components.sensor import DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    CONF_UNIQUE_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.setup import async_setup_component

from custom_components.unavailable_entities.sensor import ATTR_ENTITIES, DEFAULT_NAME


async def setup_test_entities(hass: HomeAssistant, config: Dict[str, Any] = {}) -> None:
    assert await async_setup_component(
        hass,
        DOMAIN,
        {
            "sensor": {
                "platform": "unavailable_entities",
                **config,
            },
        },
    )

    await hass.async_block_till_done()
    await hass.async_start()
    await hass.async_block_till_done()


async def test_sensor_manual_update(hass: HomeAssistant) -> None:
    await async_setup_component(hass, "homeassistant", {})
    await setup_test_entities(hass)

    await hass.services.async_call(
        "homeassistant",
        "update_entity",
        {ATTR_ENTITY_ID: ["sensor.unavailable_entities"]},
        blocking=True,
    )
    state = hass.states.get("sensor.unavailable_entities")
    assert int(state.state) == 0
    assert state.attributes[ATTR_ENTITIES] == set()

    sensors = {
        "binary_sensor.test": "off",
        "media_player.test": "off",
        "sensor.test": "off",
    }

    for sensor_id, sensor_state in sensors.items():
        hass.states.async_set(sensor_id, sensor_state)

    await hass.async_block_till_done()
    await hass.services.async_call(
        "homeassistant",
        "update_entity",
        {ATTR_ENTITY_ID: ["sensor.unavailable_entities"]},
        blocking=True,
    )
    state = hass.states.get("sensor.unavailable_entities")
    assert int(state.state) == 0
    assert state.attributes[ATTR_ENTITIES] == set()

    for sensor_id in sensors:
        hass.states.async_set(sensor_id, "unavailable")

    await hass.async_block_till_done()
    await hass.services.async_call(
        "homeassistant",
        "update_entity",
        {ATTR_ENTITY_ID: ["sensor.unavailable_entities"]},
        blocking=True,
    )
    state = hass.states.get("sensor.unavailable_entities")
    assert int(state.state) == len(sensors)
    assert state.attributes[ATTR_ENTITIES] == sensors.keys()


async def test_sensor_defaults(hass: HomeAssistant) -> None:
    await setup_test_entities(hass)

    state = hass.states.get("sensor.unavailable_entities")
    assert state
    assert state.entity_id == "sensor.unavailable_entities"
    assert state.name == DEFAULT_NAME
    assert state.attributes.get(ATTR_ICON) == "mdi:check-circle"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is None


async def test_sensor_customizations(hass: HomeAssistant) -> None:
    sensor_name = "Test Sensor"

    await setup_test_entities(hass, {CONF_NAME: sensor_name})

    state = hass.states.get("sensor.unavailable_entities")
    assert state
    assert state.entity_id == "sensor.unavailable_entities"
    assert state.name == sensor_name


async def test_sensor_unique_id(hass: HomeAssistant) -> None:
    unique_id = "abc123"

    await setup_test_entities(hass, {CONF_UNIQUE_ID: unique_id})

    registry = entity_registry.async_get(hass)
    assert registry.async_get_entity_id("sensor", "unavailable_entities", unique_id)
