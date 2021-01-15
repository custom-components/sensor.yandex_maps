"""
A platform which give you the time it will take to drive.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.yandex_maps
"""
import logging

import re

import aiohttp
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.const import TIME_MINUTES, TIME_HOURS

coords_re = re.compile(r'-?\d{1,2}\.\d{1,6},\s?-?\d{1,3}\.\d{1,6}')

__version__ = '0.0.7'

CONF_NAME = 'name'
CONF_START = 'start'
CONF_DESTINATION = 'destination'
CONF_COMMON_FORMAT = 'use_common_format'
DEFAULT_COMMON_FORMAT = False

ICON = 'mdi:car'

BASE_URL = 'https://yandex.ru/geohelper/api/v1/router?points={}~{}'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_START): cv.string,
    vol.Required(CONF_DESTINATION): cv.string,
    vol.Optional(CONF_COMMON_FORMAT, default=DEFAULT_COMMON_FORMAT): cv.boolean,
})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    name = config['name']
    start = config['start']
    destination = config['destination']
    use_common_format = config['use_common_format']

    async_add_entities(
        [YandexMapsSensor(hass, name, start, destination, use_common_format)], True)


class YandexMapsSensor(Entity):
    """YandexMap Sensor class"""

    def __init__(self, hass, name, start, destination, use_common_format):
        self.hass = hass
        self._state = None
        self._name = name
        self._start = start
        self._destination = destination
        self._use_common_format = use_common_format
        self.attr = {}
        _LOGGER.debug('Initialized sensor %s with %s, %s', self._name, self._start, self._destination)

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug('%s - Running update', self._name)
        if self.start is None or self.destination is None:
            _LOGGER.debug('%s - Could not update - wrong coordinates', self._name)
            return

        try:
            url = BASE_URL.format(self.start, self.destination)

            _LOGGER.debug('Requesting url %s', url)
            async with aiohttp.ClientSession() as client:
                async with client.get(url) as resp:
                    assert resp.status == 200
                    info = await resp.json()

                    self._state = info.get('direct', {}).get('time')
                    self.attr = {
                        'mapurl': info.get('direct', {}).get('mapUrl'),
                        'jamsrate': info.get('jamsRate'),
                        'jamsmeasure': info.get('jamsMeasure'),
                        'friendly_time': self.humanize(self._state),
                    }
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug('%s - Could not update - %s', self._name, error)

    @classmethod
    def is_coord(cls, data: str) -> bool:
        return bool(coords_re.fullmatch(data))

    @classmethod
    def humanize(cls, minutes):
        minutes = int(minutes)
        _LOGGER.debug('Passed time: %s', minutes)
        if minutes <= 60:
            return "{}{}".format(minutes, TIME_MINUTES)
        hours, reminder = divmod(minutes, 60)
        return "{}{} {}{}".format(hours, TIME_HOURS, reminder, TIME_MINUTES)

    @property
    def start(self):
        return self.point_to_coords(self._start)

    @property
    def destination(self):
        return self.point_to_coords(self._destination)

    def point_to_coords(self, point: str) -> str:
        if YandexMapsSensor.is_coord(point):
            if self._use_common_format:
                latitude, longitude = point.split(',')
                return "{},{}".format(longitude, latitude)
            return point

        state = self.hass.states.get(point)
        if state:
            latitude = state.attributes.get('latitude')
            longitude = state.attributes.get('longitude')
            if latitude and longitude:
                return "{},{}".format(longitude, latitude)
            else:
                raise AttributeError

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def unit_of_measurement(self):
        """unit_of_measurement."""
        return TIME_MINUTES

    @property
    def device_state_attributes(self):
        """Attributes."""
        return self.attr
