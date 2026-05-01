import os
import logging

import pygame


class SoundManager:
    """
    Centralised sound-effect manager for hazard and power-up sounds.

    All sound files live under ``./music/``.  Sounds are loaded lazily on
    first use (after ``pygame.mixer`` has been initialised) and cached for
    re-use.
    """

    _MUSIC_DIR = os.path.join(".", "music")

    # Maps each (level, hazard_name) pair to its sound file
    _HAZARD_SOUNDS: dict[tuple[int, str], str] = {
        # Level 1
        (1, "Meteor"):      "Level1-MeteorSound.mp3",
        (1, "RollingRock"):  "Level1-StoneSound.mp3",
        # Level 2
        (2, "Fireball"):    "Level1-MeteorSound.mp3",   # reuse meteor sound for fireball
        (2, "MammothLeg"):  "Level2-MammothSound.mp3",
        # Level 3
        (3, "Helicopter"):     "Level3-HelicopterSound.mp3",
        (3, "HelicopterTwo"):  "Level3-HelicopterSound.mp3",
        (3, "Bomb"):           "Level3-BombSound.mp3",
        (3, "Drone"):          "Level3-DroneSound.mp3",
    }

    # Maps each power-up name to its pickup sound file
    _POWERUP_SOUNDS: dict[str, str] = {
        "SlowerHazards":  "Slow Motion Sound Effect.mp3",
        "TimeReduction":  "Clock Ticking Sound Effect.mp3",
        "ShieldBubble":   "Bubble Sound Effect.mp3",
    }

    # Sound played when the shield bubble pops (expires or deflects a hit)
    _SHIELD_POP_FILE = "ShieldPopSoundEffect.mp3"

    # Volume levels — powerups/shield are slightly louder so players notice them
    _HAZARD_VOLUME  = 0.65
    _POWERUP_VOLUME = 0.75

    def __init__(self):
        self._cache: dict[str, pygame.mixer.Sound] = {}
        # Tracks how many times each hazard has reset, keyed by object id
        self._hazard_counters: dict[int, int] = {}

    def _load(self, filename: str) -> pygame.mixer.Sound | None:
        """Load a sound file from disk, cache it, and set its volume category."""
        if filename in self._cache:
            return self._cache[filename]
        path = os.path.join(self._MUSIC_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            # Powerup and shield sounds are slightly louder than hazard ambients
            if filename in self._POWERUP_SOUNDS.values() or filename == self._SHIELD_POP_FILE:
                sound.set_volume(self._POWERUP_VOLUME)
            else:
                sound.set_volume(self._HAZARD_VOLUME)
            self._cache[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError) as exc:
            logging.warning("SoundManager: could not load %s – %s", path, exc)
            return None

    def tick_hazard(self, hazard, level: int):
        """Increment the reset counter for a hazard; play its sound every 5th reset."""
        hid = id(hazard)
        self._hazard_counters[hid] = self._hazard_counters.get(hid, 0) + 1
        if self._hazard_counters[hid] % 5 == 0:
            self.play_hazard_sound(hazard.name, level)

    def play_hazard_sound(self, hazard_name: str, level: int):
        """Look up and play the sound for the given hazard in the given level."""
        key = (level, hazard_name)
        filename = self._HAZARD_SOUNDS.get(key)
        if filename is None:
            logging.debug("SoundManager: no sound mapped for %s", key)
            return
        sound = self._load(filename)
        if sound is not None:
            sound.play()

    def play_powerup_pickup(self, powerup_name: str):
        """Play the pickup sound when a power-up is collected."""
        filename = self._POWERUP_SOUNDS.get(powerup_name)
        if filename is None:
            logging.debug("SoundManager: no pickup sound for %s", powerup_name)
            return
        sound = self._load(filename)
        if sound is not None:
            sound.play()

    def play_shield_pop(self):
        """Play the pop sound when the shield bubble expires or absorbs a hit."""
        sound = self._load(self._SHIELD_POP_FILE)
        if sound is not None:
            sound.play()

    def reset_counters(self):
        """Clear all hazard reset counters (called on level reset)."""
        self._hazard_counters.clear()
