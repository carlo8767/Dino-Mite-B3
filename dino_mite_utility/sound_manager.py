import os
import logging

import pygame


class SoundManager:
    """
    Centralised sound-effect manager for hazard and power-up sounds.

    All sound files live under ``./music/``.  Sounds are loaded lazily on
    first use (after ``pygame.mixer`` has been initialised) and cached for
    re-use.

    Usage
    -----
    >>> sfx = SoundManager()
    >>> sfx.play_hazard_sound("Meteor", level=1)   # plays Level1-MeteorSound.mp3
    >>> sfx.play_powerup_pickup("ShieldBubble")     # plays Bubble Sound Effect.mp3
    >>> sfx.play_shield_pop()                        # plays ShieldPopSoundEffect.mp3
    """

    _MUSIC_DIR = os.path.join(".", "music")

    # ── Hazard sound file mapping  (level, hazard_name) → filename ──────────
    _HAZARD_SOUNDS: dict[tuple[int, str], str] = {
        # Level 1
        (1, "Meteor"):      "Level1-MeteorSound.mp3",
        (1, "RollingRock"): "Level1-StoneSound.mp3",
        # Level 2
        (2, "Fireball"):    "Level1-MeteorSound.mp3",   # reuse meteor sound for fireball
        (2, "BigArm"):      "Level2-MammothSound.mp3",
        # Level 3
        (3, "Helicopter"):    "Level3-HelicopterSound.mp3",
        (3, "HelicopterTwo"): "Level3-HelicopterSound.mp3",
        (3, "Bomb"):          "Level3-BombSound.mp3",
        (3, "Drone"):         "Level3-DroneSound.mp3",
    }

    # ── Power-up pickup sounds ──────────────────────────────────────────────
    _POWERUP_SOUNDS: dict[str, str] = {
        "SlowerHazards":  "Slow Motion Sound Effect.mp3",
        "TimeReduction":  "Clock Ticking Sound Effect.mp3",
        "ShieldBubble":   "ShieldPopSoundEffect.mp3",
    }

    _SHIELD_POP_FILE = "Bubble Sound Effect.mp3"

    # ── Volume hierarchy ─────────────────────────────────────────────────────
    # Hazard ambients sit under background music; powerups/shield cut through.
    _HAZARD_VOLUME  = 0.18
    _POWERUP_VOLUME = 0.55
    _SHIELD_VOLUME  = 0.65

    # Per-file overrides (applied after the category default)
    _VOLUME_OVERRIDES: dict[str, float] = {
        "Level1-StoneSound.mp3":      0.10,   # rolling rock is very continuous — keep low
        "Level3-HelicopterSound.mp3": 0.12,
        "Level3-DroneSound.mp3":      0.12,
        "Level3-BombSound.mp3":       0.13,
        "Level2-MammothSound.mp3":    0.20,
    }

    def __init__(self):
        self._cache: dict[str, pygame.mixer.Sound] = {}

    # ── internal helpers ────────────────────────────────────────────────────

    def _load(self, filename: str) -> pygame.mixer.Sound | None:
        """Load (and cache) a sound file; return *None* on failure."""
        if filename in self._cache:
            return self._cache[filename]
        path = os.path.join(self._MUSIC_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)

            # Determine volume category, then apply any per-file override
            if filename == self._SHIELD_POP_FILE:
                vol = self._SHIELD_VOLUME
            elif filename in self._POWERUP_SOUNDS.values():
                vol = self._POWERUP_VOLUME
            else:
                vol = self._HAZARD_VOLUME
            sound.set_volume(self._VOLUME_OVERRIDES.get(filename, vol))

            self._cache[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError) as exc:
            logging.warning("SoundManager: could not load %s – %s", path, exc)
            return None

    # ── public API ──────────────────────────────────────────────────────────

    def tick_hazard(self, hazard, level: int):
        """
        Call this every time a hazard *resets* (appears again on screen).

        Every 5th appearance the corresponding hazard sound is played.
        """
        hid = id(hazard)
        self._hazard_counters[hid] = self._hazard_counters.get(hid, 0) + 1
        if self._hazard_counters[hid] % 5 == 0:
            self.play_hazard_sound(hazard.name, level)

    def play_hazard_sound(self, hazard_name: str, level: int):
        key = (level, hazard_name)
        filename = self._HAZARD_SOUNDS.get(key)
        if filename is None:
            logging.debug("SoundManager: no sound mapped for %s", key)
            return
        sound = self._load(filename)
        if sound is not None:
            sound.play()

    def play_powerup_pickup(self, powerup_name: str):
        """Play the pickup sound for the given power-up type."""
        filename = self._POWERUP_SOUNDS.get(powerup_name)
        if filename is None:
            logging.debug("SoundManager: no pickup sound for %s", powerup_name)
            return
        sound = self._load(filename)
        if sound is not None:
            sound.play()

    def play_shield_pop(self):
        """Play the bubble-pop sound (shield expired or deflected a hazard)."""
        sound = self._load(self._SHIELD_POP_FILE)
        if sound is not None:
            sound.play()

    def play_looping(self, hazard_name: str, level: int, channel: pygame.mixer.Channel):
        """Play sound on a dedicated channel only if the channel is not already busy."""
        if channel.get_busy():
            return
        filename = self._HAZARD_SOUNDS.get((level, hazard_name))
        if filename is None:
            return
        sound = self._load(filename)
        if sound is not None:
            channel.play(sound)

    def reset_counters(self):
        """Clear all hazard appearance counters (call on level reset)."""
        self._hazard_counters.clear()
