import logging
import random

import pygame

from dino_mite_model.character_game.power_ups import SlowerHazards


class BaseLevelController:
    """
    Shared logic for all level controllers: music, pause, player input,
    collision detection, powerup deck system, and hazard slowdown.

    Subclass contract
    -----------------
    1. Set self.level_model BEFORE calling super().__init__():

        class ControllerLevelTwo(BaseLevelController):
            def __init__(self):
                self.level_model = LevelTwo()
                super().__init__()

    2. Implement register_slowable_hazards() to fill self.slowed_hazards
       with every hazard sprite in the level:

        def register_slowable_hazards(self):
            self.slowed_hazards = [
                self.level_model.hazard_???,
                ...
            ]

    Everything else (collision registry, movement, reset) is derived
    automatically from self.slowed_hazards.
    """

    def __init__(self):
        self.is_paused = False
        self.models_collision = {}

        # Slowdown powerup state
        self.slow_hazards_active = False
        self.slow_hazards_timer  = 0
        self.slow_factor         = 0.5
        self.slowed_hazards      = []
        self.original_hazard_speeds = {}

        # Subclass fills self.slowed_hazards — must run before _build_collision_registry
        self.register_slowable_hazards()
        self._build_collision_registry()

        # Deck: 3 shields, 1 time reduction, 1 slow — shuffled, auto-refills
        self._deck = self._build_deck()
        self.current_powerup        = None
        self.powerup_spawn_timer    = 0
        self.powerup_spawn_interval = 8000  # ms between spawns

    # ==================== MUSIC ====================

    def init_music(self):
        pygame.mixer.music.load(self.level_model.sound)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1, 0.0)

    def init_music_end_level(self):
        pygame.mixer.music.load(self.level_model.sound_end_game)
        pygame.mixer.music.play(-1, 0.0)

    def stop_music(self):
        pygame.mixer.music.stop()

    # ==================== PAUSE ====================

    def toggle_pause_menu(self):
        self.is_paused = not self.is_paused

    # ==================== PLAYER INPUT ====================

    def handle_player_input(self, keys, events):
        self.level_model.character.handle_key_input(keys, events)

    def apply_player_gravity(self):
        self.level_model.character.gravity()

    def apply_change_player_status(self, window, status):
        self.level_model.character.draw_status(window, status)

        # ==================== PLAYER TWO ====================

    def handle_player_input_two(self, keys, events):
        self.level_model.characterTwo.handle_key_input(keys, events)

    def apply_player_gravity_two(self):
        self.level_model.characterTwo.gravity()

    def apply_change_player_status_two(self, window, status):
        self.level_model.characterTwo.draw_status(window, status)

    # ==================== MOVEMENT ====================

    def update_movement(self):
        """Move every hazard in the level."""
        for hazard in self.slowed_hazards:
            hazard.update_position()

    # ==================== COLLISION ====================

    def _build_collision_registry(self):
        """
        Derives models_collision from slowed_hazards.
        Called once during __init__ after register_slowable_hazards().
        """
        # THIS VARIABLE DOES NOT EXIST HERE MAGIC THAT WORK
        self.models_collision[self.level_model.character] = self.level_model.character.name
        self.models_collision[self.level_model.characterTwo] = self.level_model.characterTwo.name
        for hazard in self.slowed_hazards:
            self.models_collision[hazard] = hazard.name

    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        """
        Returns (True, hazard_name) if the character collides with a hazard.
        If the shield is active, deflects the hazard and returns (False, '').
        """
        for hazard, name in self.models_collision.items():
            if name == "Dino"  or name == "Dina":
                continue
            group = pygame.sprite.Group()
            group.add(hazard)
            if pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask):
                logging.info(f"Collision detected between {sprite} and {name}")
                if sprite.shield_active:
                    logging.info(f"Shield blocked collision with {name}")
                    hazard.update_position_collision()
                    return False, ""
                return True, name
        return False, ""

    def update_collision_position(self, name):
        """Reset the position of every hazard that matches the given name."""
        for hazard, hazard_name in self.models_collision.items():
            if hazard_name == name:
                hazard.update_position_collision()

    # ==================== POWERUP LOGIC ====================

    def _build_deck(self) -> list:
        """One deck = 5 cards: 3 shields, 1 time reduction, 1 slow.
        Shuffled so the order is unpredictable but the 60/20/20 ratio is exact."""
        deck = (
            [self.level_model.pw_up_shield_bubble]  * 3 +
            [self.level_model.pw_up_time_reduction] * 1 +
            [self.level_model.pw_up_slower_hazard]  * 1
        )
        random.shuffle(deck)
        return deck

    def _spawn_powerup(self):
        if not self._deck:
            self._deck = self._build_deck()
        chosen = self._deck.pop()
        chosen.activate()
        self.current_powerup = chosen

    def update_powerup(self, delta_time: int, wild_card_character):
        """Tick shield and slowdown timers; advance the powerup spawn cycle."""
        character = wild_card_character

        if character.shield_active:
            character.shield_timer -= delta_time
            if character.shield_timer <= 0:
                character.shield_active = False
                character.shield_timer  = 0

        if self.slow_hazards_active:
            self.slow_hazards_timer -= delta_time
            if self.slow_hazards_timer <= 0:
                self.slow_hazards_active = False
                self.slow_hazards_timer  = 0
                self.restore_hazard_speeds()

        if self.current_powerup is None or not self.current_powerup.is_active:
            self.powerup_spawn_timer += delta_time
            if self.powerup_spawn_timer >= self.powerup_spawn_interval:
                self._spawn_powerup()
                self.powerup_spawn_timer = 0
        else:
            self.current_powerup.update_position()

    def detection_collision_powerup(self, wild_card_sprite) -> str:
        """Returns the name of the collected powerup, or '' if none was collected."""
        if self.current_powerup is None or not self.current_powerup.is_active:
            return ""
        group = pygame.sprite.Group()
        group.add(self.current_powerup)
        if pygame.sprite.spritecollide(
            # THIS MAGIC
                wild_card_sprite, group, False, pygame.sprite.collide_mask):
            name = self.current_powerup.name
            #self.current_powerup.apply_effect(self.level_model.character)
            # EMPTY METHOD  YOU CAN DELETE
            self.current_powerup.apply_effect(wild_card_sprite)
            if isinstance(self.current_powerup, SlowerHazards):
                self.slow_hazards_active = True
                self.slow_hazards_timer  = 5000
                self.apply_slow_hazards()
            self.current_powerup.update_position_collision()
            self.current_powerup = None
            logging.info(f"Powerup collected: {name}")
            return name
        return ""

    # ==================== SLOWDOWN HELPERS ====================

    def _get_speed_attr(self, hazard) -> str | None:
        """Returns the name of the speed attribute on a hazard, or None."""
        if hasattr(hazard, "speed"):
            return "speed"
        if hasattr(hazard, "move_x"):
            return "move_x"
        return None

    def apply_slow_hazards(self):
        for hazard in self.slowed_hazards:
            attr = self._get_speed_attr(hazard)
            if attr is None:
                continue
            if hazard not in self.original_hazard_speeds:
                self.original_hazard_speeds[hazard] = getattr(hazard, attr)
            slowed = max(1, int(self.original_hazard_speeds[hazard] * self.slow_factor))
            setattr(hazard, attr, slowed)

    def restore_hazard_speeds(self):
        for hazard, original_speed in self.original_hazard_speeds.items():
            attr = self._get_speed_attr(hazard)
            if attr is not None:
                setattr(hazard, attr, original_speed)

    # ==================== LEVEL RESET ====================

    def reset_level(self):
        """Reset the character and all hazards to their starting positions."""
        char = self.level_model.character
        char.rect.center  = (char.position_x, char.constant_ground)
        char.game_state   = "idle"
        char.speed_y      = 0
        char.png_on_ground = True
        char.shield_active = False
        char.shield_timer  = 0

        for hazard in self.slowed_hazards:
            hazard.update_position_collision()

        self.slow_hazards_active = False
        self.slow_hazards_timer  = 0
        self.restore_hazard_speeds()

    # ==================== ABSTRACT ====================

    def register_slowable_hazards(self):
        """
        Subclasses must override this to populate self.slowed_hazards with
        every hazard sprite in the level. Called once during __init__.

        Example:
            def register_slowable_hazards(self):
                self.slowed_hazards = [
                    self.level_model.hazard_meteor,
                    self.level_model.hazard_rollingRock,
                ]
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement register_slowable_hazards()"
        )
