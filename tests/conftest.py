import pytest


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
# pylint: disable=unused-argument
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield
