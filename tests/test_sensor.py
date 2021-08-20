from homeassistant.setup import async_setup_component


async def test_entity(hass):
    assert await async_setup_component(
        hass,
        "sensor",
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
    assert state.state == "0"
