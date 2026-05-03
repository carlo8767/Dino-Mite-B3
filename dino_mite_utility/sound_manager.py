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

    # Lookup table: (level_number, hazard_name) → audio filename
    _HAZARD_SOUNDS: dict[tuple[int, str], str] = {
        (1, "RollingRock"):  "Level1-StoneSound.mp3",
        (2, "BigArm"):       "BigArmSoundEffect.mp3",
        (3, "Helicopter"):   "Level3-HelicopterSound.mp3",
        (3, "HelicopterTwo"):"Level3-HelicopterSound.mp3",
        (3, "Drone"):        "Level3-DroneSound.mp3",
    }

    # Lookup table: power-up name → pickup audio filename
    _POWERUP_SOUNDS: dict[str, str] = {
        "SlowerHazards":  "Slow Motion Sound Effect.mp3",
    }

    # Default volume levels for each sound category
    _HAZARD_VOLUME  = 0.30
    _POWERUP_VOLUME = 0.55

    # Per-file volume overrides (takes priority over the category default)
    _VOLUME_OVERRIDES: dict[str, float] = {
        "Level1-StoneSound.mp3":      0.02,
        "Level3-HelicopterSound.mp3": 0.05,
        "Level3-DroneSound.mp3":      0.10,
        "BigArmSoundEffect.mp3":      0.20,
    }

    def __init__(self):
        # Cache of already loaded Sound objects keyed by filename
        self._cache: dict[str, pygame.mixer.Sound] = {}

    def _load(self, filename: str) -> pygame.mixer.Sound | None:
        """Return a cached Sound for filename, loading it from disk on first access."""
        if filename in self._cache:
            return self._cache[filename]
        path = os.path.join(self._MUSIC_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)

            # Pick the right category volume, then let per-file override win
            if filename in self._POWERUP_SOUNDS.values():
                vol = self._POWERUP_VOLUME
            else:
                vol = self._HAZARD_VOLUME
            sound.set_volume(self._VOLUME_OVERRIDES.get(filename, vol))

            self._cache[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError) as exc:
            logging.warning("SoundManager: could not load %s – %s", path, exc)
            return None

    def play_powerup_pickup(self, powerup_name: str):
        """Play the one-shot pickup jingle for the given power-up type."""
        filename = self._POWERUP_SOUNDS.get(powerup_name)
        if filename is None:
            logging.debug("SoundManager: no pickup sound for %s", powerup_name)
            return
        sound = self._load(filename)
        if sound is not None:
            sound.play()

    def play_looping(self, hazard_name: str, level: int, channel: pygame.mixer.Channel):
        """Start a hazard sound on channel only if the channel is currently idle."""
        if channel.get_busy():
            return
        filename = self._HAZARD_SOUNDS.get((level, hazard_name))
        if filename is None:
            return
        sound = self._load(filename)
        if sound is not None:
            channel.play(sound)
