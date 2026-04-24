import pygame
import logging
import random

from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_model.character_game.power_ups import SlowerHazards


class ControllerLevelOne:

    def __init__(self):
        self.level_one = LevelOne()
        self.is_paused = False
        self.models_collision = dict()

        # Dynamic hazard lists (for any spawned-at-runtime hazards)
        self.meteors = []
        self.rolling_rocks = []

        self.add_models_collision()

        # Shuffled deck: 3 shields, 1 time reduction, 1 slow per 5 spawns.
        # Guarantees exact 60/20/20 split — deck refills automatically when empty.
        # Uses the same 3 instances every time, no new objects created mid-game.
        self._deck = self._build_deck()
        self.current_powerup = None
        self.powerup_spawn_timer = 0
        self.powerup_spawn_interval = 8000   # spawn every 8s — ensures 2 full decks fit in 2 min

        # Slowdown powerup state
        self.slow_hazards_active = False
        self.slow_hazards_timer = 0
        self.slow_factor = 0.5
        self.slowed_hazards = []
        self.original_hazard_speeds = {}
        self.register_slowable_hazards()

    # ==================== MUSIC ====================

    def init_music(self):
        pygame.mixer.music.load(self.level_one.sound)
        pygame.mixer.music.play(-1, 0.0)

    def init_music_end_level_one(self):
        pygame.mixer.music.load(self.level_one.sound_end_game)
        pygame.mixer.music.play(-1, 0.0)

    def stop_music(self):
        pygame.mixer.music.stop()

    # ==================== PAUSE ====================

    def toggle_pause_menu(self):
        self.is_paused = not self.is_paused

    # ==================== PLAYER INPUT ====================

    def handle_player_input(self, keys, events):
        self.level_one.character.handle_key_input(keys, events)

    def apply_player_gravity(self):
        self.level_one.character.gravity()

    def apply_change_player_status(self, window, status):
        self.level_one.character.draw_status(window, status)

    # ==================== MOVEMENT ====================

    def update_movement_level_one(self):
        self.level_one.hazard_meteor.update_position()
        self.level_one.hazard_meteorOne.update_position()
        self.level_one.hazard_meteorTwo.update_position()
        self.level_one.hazard_rollingRock.update_position()
        for rock in self.rolling_rocks:
            rock.update_position()

    # ==================== COLLISION ====================

    def add_models_collision(self):
        """Register hazards only — powerups are checked separately via detection_collision_powerup."""
        self.models_collision[self.level_one.character] = self.level_one.character.name
        self.models_collision[self.level_one.hazard_meteor] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorOne] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorTwo] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_rollingRock] = self.level_one.hazard_rollingRock.name

    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        """
        Check if the character collides with any hazard.
        If the shield is active, deflect the hazard instead of triggering game over.
        """
        for hazard, name in self.models_collision.items():
            if hazard == sprite:
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
        for hazard, hazard_name in self.models_collision.items():
            if hazard_name == name:
                hazard.update_position_collision()

    # ==================== POWERUP LOGIC ====================

    def _build_deck(self) -> list:
        # One deck = 5 cards: 3 shields, 1 time reduction, 1 slow hazards.
        # Shuffled so the order is unpredictable but the ratio is always exact.
        deck = (
            [self.level_one.pw_up_shield_bubble] * 3 +
            [self.level_one.pw_up_time_reduction] * 1 +
            [self.level_one.pw_up_slower_hazard]  * 1
        )
        random.shuffle(deck)
        return deck

    def _spawn_powerup(self):
        if not self._deck:
            self._deck = self._build_deck()  # refill and reshuffle when deck runs out
        chosen = self._deck.pop()
        chosen.activate()
        self.current_powerup = chosen

    def update_powerup(self, delta_time):
        character = self.level_one.character

        # Tick shield timer down
        if character.shield_active:
            character.shield_timer -= delta_time
            if character.shield_timer <= 0:
                character.shield_active = False
                character.shield_timer = 0

        # Tick slowdown timer down
        if self.slow_hazards_active:
            self.slow_hazards_timer -= delta_time
            if self.slow_hazards_timer <= 0:
                self.slow_hazards_active = False
                self.slow_hazards_timer = 0
                self.restore_hazard_speeds()

        # Advance spawn timer or move the active powerup
        if self.current_powerup is None or not self.current_powerup.is_active:
            self.powerup_spawn_timer += delta_time
            if self.powerup_spawn_timer >= self.powerup_spawn_interval:
                self._spawn_powerup()
                self.powerup_spawn_timer = 0
        else:
            self.current_powerup.update_position()

    def detection_collision_powerup(self) -> str:
        """Returns the name of the collected powerup, or '' if none collected."""
        if self.current_powerup is None or not self.current_powerup.is_active:
            return ""
        group = pygame.sprite.Group()
        group.add(self.current_powerup)
        if pygame.sprite.spritecollide(
                self.level_one.character, group, False, pygame.sprite.collide_mask):
            name = self.current_powerup.name
            self.current_powerup.apply_effect(self.level_one.character)
            if isinstance(self.current_powerup, SlowerHazards):
                self.slow_hazards_active = True
                self.slow_hazards_timer = 5000
                self.apply_slow_hazards()
            self.current_powerup.update_position_collision()
            self.current_powerup = None
            logging.info(f"Powerup collected: {name}")
            return name
        return ""

    # ==================== SLOWDOWN HELPERS ====================

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_one.hazard_meteor,
            self.level_one.hazard_meteorOne,
            self.level_one.hazard_meteorTwo,
            self.level_one.hazard_rollingRock,
        ] + self.meteors + self.rolling_rocks

    def _get_speed_attr(self, hazard):
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
        char = self.level_one.character
        char.rect.center = (char.position_x, char.constant_ground)
        char.game_state = "idle"
        char.speed_y = 0
        char.png_on_ground = True
        char.shield_active = False
        char.shield_timer = 0

        self.level_one.hazard_meteor.update_position_collision()
        self.level_one.hazard_meteorOne.update_position_collision()
        self.level_one.hazard_meteorTwo.update_position_collision()
        self.level_one.hazard_rollingRock.update_position_collision()

        self.slow_hazards_active = False
        self.slow_hazards_timer = 0
        self.restore_hazard_speeds()
