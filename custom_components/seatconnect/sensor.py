"""
Support for Seat Connect Platform
"""
import logging

from . import DATA_KEY, DOMAIN, SeatEntity
from .const import DATA
from homeassistant.const import CONF_RESOURCES

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Seat sensors."""
    if discovery_info is None:
        return
    async_add_entities([SeatSensor(hass.data[DATA_KEY], *discovery_info)])


async def async_setup_entry(hass, entry, async_add_devices):
    data = hass.data[DOMAIN][entry.entry_id][DATA]
    coordinator = data.coordinator
    if coordinator.data is not None:
        if CONF_RESOURCES in entry.options:
            resources = entry.options[CONF_RESOURCES]
        else:
            resources = entry.data[CONF_RESOURCES]

        async_add_devices(
            SeatSensor(
                data, instrument.vehicle_name, instrument.component, instrument.attr
            )
            for instrument in (
                instrument
                for instrument in data.instruments
                if instrument.component == "sensor" and instrument.attr in resources
            )
        )

    return True


class SeatSensor(SeatEntity):
    """Representation of a Seat Sensor."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.instrument.state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.instrument.unit
