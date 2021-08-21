from homeassistant.components.sensor import DOMAIN
from homeassistant.const import ATTR_ICON, ATTR_UNIT_OF_MEASUREMENT
from homeassistant.setup import async_setup_component

from custom_components.unavailable_entities.sensor import UnavailableEntitiesSensor


async def test_sensor(hass):
    sensor = UnavailableEntitiesSensor(hass)

    await hass.async_block_till_done()
    await hass.async_start()
    await hass.async_block_till_done()

    sensor.async_schedule_update_ha_state(True)
    await hass.async_block_till_done()
    assert sensor.state == 0

    sensors = {
        "binary_sensor.test": "off",
        "media_player.test": "off",
        "sensor.test": "off",
    }

    for sensor_id, sensor_state in sensors.items():
        hass.states.async_set(sensor_id, sensor_state)
    sensor.async_schedule_update_ha_state(True)
    await hass.async_block_till_done()
    assert sensor.state == 0

    for sensor_id in sensors:
        hass.states.async_set(sensor_id, "unavailable")
    sensor.async_schedule_update_ha_state(True)
    await hass.async_block_till_done()
    assert sensor.state == len(sensors)


async def test_sensor_defaults(hass):
    assert await async_setup_component(
        hass,
        DOMAIN,
        {
            "sensor": {
                "platform": "unavailable_entities",
            },
        },
    )

    await hass.async_block_till_done()
    await hass.async_start()
    await hass.async_block_till_done()

    state = hass.states.get("sensor.unavailable_entities")
    assert state.entity_id == "sensor.unavailable_entities"
    assert state.name == "unavailable entities"
    assert state.attributes.get(ATTR_ICON) == "mdi:check-circle"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is None
    assert state.state == "0"
