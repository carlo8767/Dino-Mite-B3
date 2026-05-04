import logging
from abc import ABC, abstractmethod

import pygame

from dino_mite_model.character_game.power_ups import SlowerHazards
from dino_mite_utility.sound_manager import SoundManager


class BaseLevelController(ABC):
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
        self.game_over_one_player_mode = False
        self.two_players_game_over_mode = False
        self.player_one_active = False
        self.player_two_active = False
        self.time_reduction_ms = 0
        self.show_time_reduction_hud = 0
        self.models_collision = {}

        # Slowdown powerup state
        self.slow_hazards_active = False
        self.slow_hazards_timer  = 0
        self.slow_factor         = 0.5
        self.slowed_hazards      = []
        self.original_hazard_speeds = {}

        # Subclass fills self.slowed_hazards - must run before _build_collision_registry
        self.register_slowable_hazards()
        self.add_models_collision_hazard()

        # Deck: 3 shields, 1 time reduction, 1 slow - shuffled, auto-refills
        self._deck = self._build_deck()
        self.current_powerup        = None
        self.powerup_spawn_timer    = 0
        self.powerup_spawn_interval = 8000  # ms between spawns
        self.sound_manager          = SoundManager()

    # ==================== MUSIC ====================
    @abstractmethod
    def init_music(self):
        pass
    @abstractmethod
    def init_music_end_level(self):
        pass

    def stop_music(self):
        pygame.mixer.music.stop()

    # ==================== PAUSE ====================

    def toggle_pause_menu(self):
        self.is_paused = not self.is_paused

    # ==================== PLAYER INPUT ====================

    def handle_player_input(self, keys, events):
        char = self.level_model.character
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and char.png_on_ground:
                    char.start_jump()
                if event.key == pygame.K_s and char.png_on_ground:
                    char.start_duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s and char.game_state == "duck":
                    char.stop_duck()
        if char.game_state == "duck" and pygame.time.get_ticks() - char.duck_start_ticks >= 1000:
            char.stop_duck()
        if keys[pygame.K_a]:
            char.walk_left()
        elif keys[pygame.K_d]:
            char.walk_right()
        else:
            char.set_idle()

    def apply_player_gravity(self):
        self.level_model.character.gravity()

    def apply_change_player_status(self, window, status):
        self.level_model.character.draw_status(window, status)

    # ==================== PLAYER TWO ====================

    def handle_player_input_two(self, keys, events):
        char = self.level_model.characterTwo
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and char.png_on_ground:
                    char.start_jump()
                if event.key == pygame.K_DOWN and char.png_on_ground:
                    char.start_duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and char.game_state == "duck":
                    char.stop_duck()
        if char.game_state == "duck" and pygame.time.get_ticks() - char.duck_start_ticks >= 1000:
            char.stop_duck()
        if keys[pygame.K_LEFT]:
            char.walk_left()
        elif keys[pygame.K_RIGHT]:
            char.walk_right()
        else:
            char.set_idle()

    def apply_player_gravity_two(self):
        self.level_model.characterTwo.gravity()

    def apply_change_player_status_two(self, window, status):
        self.level_model.characterTwo.draw_status(window, status)

    # ==================== GAME UPDATE ====================
    def input_players(self, keys, events):
        if self.get_player_two_status():
            self.handle_player_input_two(keys, events)
            self.apply_player_gravity_two()
        if self.get_player_one_status():
            self.handle_player_input(keys, events)
            self.apply_player_gravity()

    def detection_collision_power_up(self, delta_time):
            self.update_powerup(delta_time, self.level_model.character)
            self.update_powerup(delta_time, self.level_model.characterTwo)

            if self.get_player_one_status():
                collected = self.detection_collision_powerup(self.level_model.character)
                if collected == "TimeReduction":
                    self.time_reduction_ms += 5000
                    self.show_time_reduction_hud = 1000
                if collected:
                    self.sound_manager.play_powerup_pickup(collected)
            if self.get_player_two_status():
                collected = self.detection_collision_powerup(self.level_model.characterTwo)
                if collected == "TimeReduction":
                    self.time_reduction_ms += 5000
                    self.show_time_reduction_hud = 2000
                if collected:
                    self.sound_manager.play_powerup_pickup(collected)

            if self.show_time_reduction_hud > 0:
                self.show_time_reduction_hud = max(0, self.show_time_reduction_hud - delta_time)



    def update_hazard_movement(self):
        """Single game-logic, called once per frame by the view's main loop."""
        self.update_movement_hazard()


    def check_hazard_collisions_update(self, active_player_player_two_mode):
            collided_one, name_one = False, ""
            collided_two, name_two = False, ""

            if self.get_player_two_status():
                collided_two, name_two = self.detection_collision_character(self.level_model.characterTwo)

            if self.get_player_one_status():
                collided_one, name_one = self.detection_collision_character(self.level_model.character)
            if collided_one :
                self.set_player_one_status(False)
                self.update_collision_position(name_one)
            if collided_two:
                self.set_player_two_status(False)
                self.update_collision_position(name_two)
            if not active_player_player_two_mode and collided_one:
                self.stop_music()
                pygame.mixer.stop()
                self.set_game_over_one_player_mode(True)
            if active_player_player_two_mode and not self.get_player_two_status() and not self.get_player_one_status():
                self.stop_music()
                pygame.mixer.stop()
                self.set_game_over_two_players_mode(True)

    # ==================== MOVEMENT ====================

    def update_movement_hazard(self):
        """Move every hazard in the level."""
        for hazard in self.slowed_hazards:
            hazard.update_position()

    # ==================== COLLISION ====================

    def add_models_collision_hazard(self):
        """
        Derives models_collision from slowed_hazards.
        Called once during __init__ after register_slowable_hazards().
        """
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
            if name == "Dino" or name == "Dina":
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
        if pygame.sprite.spritecollide(wild_card_sprite, group, False, pygame.sprite.collide_mask):
            name = self.current_powerup.name
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

    def set_player_two_status(self, status):
        self. player_two_active = status

    def get_player_two_status(self)->bool:
        return self.player_two_active

    def set_player_one_status(self, status):
        self.player_one_active = status

    def get_player_one_status(self):
        return self.player_one_active

    def set_game_over_one_player_mode(self, status):
        self.game_over_one_player_mode = status

    def get_game_over_one_player_mode(self):
        return self.game_over_one_player_mode

    def set_game_over_two_players_mode(self, status):
        self.two_players_game_over_mode = status

    def get_two_players_game_over_mode(self):
        return self.two_players_game_over_mode

    # # ==================== LEVEL RESET ====================
    #
    # def reset_level(self):
    #     """Reset the character and all hazards to their starting positions."""
    #     char = self.level_model.character
    #     char.rect.center  = (char.position_x, char.constant_ground)
    #     char.game_state   = "idle"
    #     char.speed_y      = 0
    #     char.png_on_ground = True
    #     char.shield_active = False
    #     char.shield_timer  = 0
    #
    #     for hazard in self.slowed_hazards:
    #         hazard.update_position_collision()
    #
    #     self.slow_hazards_active = False
    #     self.slow_hazards_timer  = 0
    #     self.restore_hazard_speeds()

    # ==================== ABSTRACT ====================

    @abstractmethod
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

    @abstractmethod
    def _build_deck(self) -> list:
        """One deck = 5 cards: 3 shields, 1 time reduction, 1 slow.
        Shuffled so the order is unpredictable but the 60/20/20 ratio is exact."""

