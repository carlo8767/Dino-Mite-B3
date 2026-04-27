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

    # ── Power-up pickup sounds ──────────────────────────────────────────────
    _POWERUP_SOUNDS: dict[str, str] = {
        "SlowerHazards":  "Slow Motion Sound Effect.mp3",
        "TimeReduction":  "Clock Ticking Sound Effect.mp3",
        "ShieldBubble":   "Bubble Sound Effect.mp3",
    }

    _SHIELD_POP_FILE = "ShieldPopSoundEffect.mp3"

    def __init__(self):
        self._cache: dict[str, pygame.mixer.Sound] = {}
        # Counters: keyed by id(hazard_object) → number of resets/appearances
        self._hazard_counters: dict[int, int] = {}

    # ── internal helpers ────────────────────────────────────────────────────

    def _load(self, filename: str) -> pygame.mixer.Sound | None:
        """Load (and cache) a sound file; return *None* on failure."""
        if filename in self._cache:
            return self._cache[filename]
        path = os.path.join(self._MUSIC_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.6)
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

    def reset_counters(self):
        """Clear all hazard appearance counters (call on level reset)."""
        self._hazard_counters.clear()
