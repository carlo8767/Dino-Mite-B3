import pygame
import logging
import random

from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_model.character_game.Hazard import Meteor, RollingRock
from dino_mite_model.character_game.power_ups import ShieldBubble, TimeReduction, SlowerHazards


class ControllerLevelOne:

    def __init__(self):
        self.level_one = LevelOne()
        self.is_paused = False
        self.models_collision = dict()

        # Dynamic hazard lists (for any spawned-at-runtime hazards)
        self.meteors = []
        self.rolling_rocks = []

        self.add_models_collision()

        # Powerup Setup
        self.current_powerup = None         # one powerup at a time
        self.powerup_spawn_timer = 0        # counts up in milliseconds
        self.powerup_spawn_interval = 15000 # spawn every 15s

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

    # ==================== MOVEMENT ====================

    def update_movement_level_one(self):
        self.level_one.hazard_meteor.update_position()
        self.level_one.hazard_meteorOne.update_position()
        self.level_one.hazard_meteorTwo.update_position()
        self.level_one.hazard_rollingRock.update_position()
        for rock in self.rolling_rocks:
            rock.update_position()

    # ==================== DYNAMIC HAZARD SPAWNING ====================

    def spawn_meteor(self):
        new_meteor = Meteor()
        self.meteors.append(new_meteor)
        self.slowed_hazards.append(new_meteor)
        self.models_collision[new_meteor] = new_meteor.name

    def spawn_rolling_rock(self):
        new_rock = RollingRock()
        self.rolling_rocks.append(new_rock)
        self.slowed_hazards.append(new_rock)
        self.models_collision[new_rock] = new_rock.name

    # ==================== COLLISION ====================

    def add_models_collision(self):
        """Register all level one sprites for collision checking"""
        self.models_collision[self.level_one.character] = self.level_one.character.name
        self.models_collision[self.level_one.hazard_meteor] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorOne] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorTwo] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_rollingRock] = self.level_one.hazard_rollingRock.name

    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        """
        Check if the character collides with any hazard
        If the shield is active, deflect the hazard and return no collision
        """
        shield_active = getattr(sprite, 'shield_active', False)
        for hazard, name in self.models_collision.items():
            if hazard == sprite:
                continue
            group = pygame.sprite.Group()
            group.add(hazard)
            if pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask):
                logging.info(f"Collision detected between {sprite} and {name}")
                if shield_active:
                    hazard.update_position_collision()
                    return False, ""
                return True, name
        return False, ""

    def update_collision_position(self, name):
        for hazard, hazard_name in self.models_collision.items():
            if hazard_name == name:
                hazard.update_position_collision()

    # ==================== LEVEL RESET ====================

    def reset_level(self):
        char = self.level_one.character
        char.rect.center = (char.position_x, char.constant_ground)
        char.game_state = "idle"
        char.speed_y = 0
        char.png_on_ground = True

        self.level_one.hazard_meteor.update_position_collision()
        self.level_one.hazard_meteorOne.update_position_collision()
        self.level_one.hazard_meteorTwo.update_position_collision()
        self.level_one.hazard_rollingRock.update_position_collision()

        self.slow_hazards_active = False
        self.slow_hazards_timer = 0
        self.restore_hazard_speeds()

    # ==================== SLOWDOWN POWERUP HELPERS ====================

    def register_slowable_hazards(self):
        """Collect all active hazards so the slowdown effect can be applied uniformly"""
        self.slowed_hazards = [
            self.level_one.hazard_meteor,
            self.level_one.hazard_meteorOne,
            self.level_one.hazard_meteorTwo,
            self.level_one.hazard_rollingRock,
        ] + self.meteors + self.rolling_rocks

    def _get_speed_attr(self, hazard):
        """Return the speed attribute name used by this hazard, or None"""
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

    # ==================== POWERUP LOGIC ====================
    
    def spawn_powerup(self):
    # spawns a random powerup: 60% shield, 20% time reduction and 20% slower hazards
        roll = random.random()
        if roll < 0.60:
            self.current_powerup = ShieldBubble()
        elif roll < 0.80:
            self.current_powerup = TimeReduction()
        else:
            self.current_powerup = SlowerHazards()

    def update_powerup(self, delta_time):
        character = self.level_one.character

        # Tick down shield timer
        if getattr(character, 'shield_active', False):
            character.shield_timer -= delta_time
            if character.shield_timer <= 0:
                character.shield_active = False
                character.shield_timer = 0

        # Tick down slowdown timer
        if self.slow_hazards_active:
            self.slow_hazards_timer -= delta_time
            if self.slow_hazards_timer <= 0:
                self.slow_hazards_active = False
                self.slow_hazards_timer = 0
                self.restore_hazard_speeds()

        # Spawn timer or move active powerup
        if self.current_powerup is None or not self.current_powerup.is_active:
            self.powerup_spawn_timer += delta_time
            if self.powerup_spawn_timer >= self.powerup_spawn_interval:
                self.spawn_powerup()
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
            powerup_name = self.current_powerup.name
            self.current_powerup.apply_effect(self.level_one.character)
            if isinstance(self.current_powerup, SlowerHazards):
                self.slow_hazards_active = True
                self.slow_hazards_timer = 5000
                self.apply_slow_hazards()
            self.current_powerup.is_active = False
            self.current_powerup = None
            logging.info(f"Powerup collected: {powerup_name}")
            return powerup_name
        return ""