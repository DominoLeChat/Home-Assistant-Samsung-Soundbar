"""samsung Soundbar MediaPlayer    """
import logging
import asyncio
import voluptuous as vol
from datetime import timedelta

# vol.Required(CONF_DEVICE_ID): cv.string,

from .api import SoundbarApi

# From homeassistant
from custom_components.samsung_soundbar import _LOGGER, DOMAIN as SOUNDBAR_DOMAIN
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_SELECT_SOUND_MODE,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
    SUPPORT_VOLUME_SET,
)
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    DEVICE_CLASS_SPEAKER,
)

import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

# VERSION
VERSION = "2.1"

# Dependencies
DEPENDENCIES = ["soundbar"]

# Return cached results if last scan was less then this time ago.
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=5)

SUPPORT_samsung_SOUNDBAR = (
    SUPPORT_PAUSE
    | SUPPORT_VOLUME_STEP
    | SUPPORT_VOLUME_MUTE
    | SUPPORT_VOLUME_SET
    | SUPPORT_SUBWOOFER_VOLUME_SET
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_SELECT_SOUND_MODE
    | SUPPORT_TURN_OFF
    | SUPPORT_TURN_ON
    | SUPPORT_PLAY
)


# SETUP PLATFORM
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up platform."""
    """Initialize the Soundbar device."""
    devices = []
    soundbar_list = hass.data[SOUNDBAR_DOMAIN]

    for device in soundbar_list:
        _LOGGER.debug("Configured a new SoundbarMediaPlayer %s", device.name)

        devices.append(SoundbarMediaPlayer(device))

    async_add_entities(devices, update_before_add=True)


# samsung Soundbar Media Player Devic


class SoundbarMediaPlayer(MediaPlayerEntity):
    def __init__(self, SoundbarMediaPlayerEntity):
        """Initialize the Soundbar device."""
        self._name = SoundbarMediaPlayerEntity.name
        self._device_id = SoundbarMediaPlayerEntity.device_id
        self._api_key = SoundbarMediaPlayerEntity.api_key
        self._max_volume = SoundbarMediaPlayerEntity.max_volume
        self._volume = 1
        self._muted = False
        self._playing = True
        self._state = "on"
        self._source = ""
        self._source_list = []
        self._sound_mode = "standard"
        self._sound_mode_list = []
        self._media_title = ""

    # Run when added to HASS TO LOAD SOURCES
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

    def update(self):
        SoundbarApi.device_update(self)

    ################################## Commandes ###############################
    ### arg , cmdtype

    def turn_off(self):
        SoundbarApi.send_command(self, "", "switch_off")

    def turn_on(self):
        SoundbarApi.send_command(self, "", "switch_on")

    def set_volume_level(self, volume_level: float):
        cmdtype = "setvolume"
        SoundbarApi.send_command(self, volume_level, cmdtype)

    def mute_volume(self, mute: bool):
        cmdtype = "audiomute"
        SoundbarApi.send_command(self, mute, cmdtype)

    def volume_up(self):
        SoundbarApi.send_command(self, "up", "stepvolume")

    def volume_down(self):
        SoundbarApi.send_command(self, "down", "stepvolume")

    def select_source(self, source: str):
        SoundbarApi.send_command(self, source, "selectsource")

    def select_sound_mode(self, sound_mode: str):
        SoundbarApi.send_command(self, sound_mode, "selectsoundmode")

    def set_subwoofer_volume(self, volume):
        SoundbarApi.send_command(self, volume, "set_subwoofer_volume")   

    def media_play(self):
        SoundbarApi.send_command(self, "", "play")

    def media_pause(self):
        SoundbarApi.send_command(self, "", "pause")

    ################################## Attributs ###############################

    @property
    def device_class(self):
        return DEVICE_CLASS_SPEAKER

    @property
    def supported_features(self):
        return SUPPORT_samsung_SOUNDBAR

    @property
    def name(self):
        return self._name

    @property
    def device_id(self):
        return self._device_id

    @property
    def api_key(self):
        return self._api_key

    @property
    def media_title(self):
        return self._media_title

    @property
    def state(self):
        return self._state

    @property
    def is_volume_muted(self):
        return self._muted

    @property
    def volume_level(self):
        return self._volume

    @property
    def source(self):
        return self._source

    @property
    def source_list(self):
        return self._source_list

    @property
    def sound_mode(self):
        return self._sound_mode

    @property
    def sound_mode_list(self):
        return self._sound_mode_list
        
    @property
    def subwoofer_volume_level(self):
        return self._subwoofer_volume
