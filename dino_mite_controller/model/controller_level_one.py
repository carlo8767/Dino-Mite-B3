from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.character_game.Hazard import RollingRock
from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_model.character_game.power_ups import ShieldBubble, TimeReduction, SlowerHazards
import random



import pygame
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ControllerLevelOne:

    def __init__(self):
        self.level_one = LevelOne()
        self.meteors = [Meteor() for _ in range(5)]  # 5 meteors always active
        self.rolling_rocks = []
        self.is_paused = False
        self.models_collision = dict()

        self.add_models_collision()

        # Powerup Setup
        self.current_powerup = None        # one powerup at a time
        self.powerup_spawn_timer = 0       # counts up in milliseconds
        self.powerup_spawn_interval = 15000 # spawn every 15s → ~8 powerups in 2 min
        self.time_penalty_ms = 0           # accumulated ms penalty applied to the timer

        # Slowdown powerup state, these variables track whether hazards are slowed and for how long
        self.slow_hazards_active = False
        self.slow_hazards_timer = 0
        self.slow_factor = 0.5

        # Store all hazards affected by the slowdown and their original speeds for reseting
        self.slowed_hazards = []
        self.original_hazard_speeds = {}
        self.register_slowable_hazards()


    def init_music(self):
        pygame.mixer.music.load(self.level_one.sound)
        pygame.mixer.music.play(-1, 0.0) # Forever Loop

    def stop_music(self):
        pygame.mixer.music.stop()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def update_movement_level_one(self):
        # Update the single model hazards (the ones actually drawn on screen)
        self.level_one.hazard_meteor.update_position()
        self.level_one.hazard_meteorOne.update_position()
        self.level_one.hazard_meteorTwo.update_position()
        # Update list-based meteors
        for meteor in self.meteors:
            meteor.update_position()

        self.level_one.hazard_rollingRock.update_position()
        # Update list-based rolling rocks, remove when off-screen
        for rock in self.rolling_rocks:
            rock.update_position()
        # self.rolling_rocks = [r for r in self.rolling_rocks if r.is_active]

    # Add newly spawned meteor to slowdown system and collision tracking
    def spawn_meteor(self):
        new_meteor = Meteor()
        self.meteors.append(new_meteor)
        self.slowed_hazards.append(new_meteor)
        self.models_collision[new_meteor] = new_meteor.name

    # Add newly spawned rolling rock to slowdown system and collision tracking
    def spawn_rolling_rock(self):
        new_rock = RollingRock()
        self.rolling_rocks.append(new_rock)
        self.slowed_hazards.append(new_rock)
        self.models_collision[new_rock] = new_rock.name
        return self.level_one

    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        # If shield is active, hazard collisions are blocked
        if getattr(sprite, 'shield_active', False):
            return False, ""
        for g, v in self.models_collision.items():
            # Skip the sprite we are testing (the character itself)
            if g == sprite:
                continue
            sprites_group = pygame.sprite.Group()
            sprites_group.add(g)
            # spritecollide returns a list of colliding sprites and remove from the group
            if pygame.sprite.spritecollide(sprite, sprites_group, False, pygame.sprite.collide_mask):
                print("collude")
                return True, v
        return False, ""

    # ==================== PLAYER INPUT (forwarded to model) ====================

    def handle_player_input(self, keys, events):
        """Forward keyboard input to the player_movement model."""
        self.level_one.character.handle_key_input(keys, events)

    def apply_player_gravity(self):
        """Forward gravity call to the player_movement model."""
        self.level_one.character.gravity()

    # ==================== SCREEN COLLISION (character) ====================

    def screen_collision_character(self, verse_x):
        """Check if the character has hit the edge of the screen."""
        x, y = self.level_one.character.get_current_position()
        return self.level_one.verification_limit_screen_colision(x, y, verse_x)

    # ==================== COLLISION HELPERS ====================

    def update_collision_position(self, name):
        [k.update_position_collision() for k, v in self.models_collision.items() if v == name]

    # ==================== SPLIT SCREEN COLLISION (hazards) ====================
    # Meteor and RollingRock have different behaviour when they leave
    # the screen, so they are handled separately.

    def screen_collision_meteor(self):
        """
        Meteor falls top to bottom.
        When it goes past the bottom of the screen, reset it back to
        the top with a new random x position (handled by update_position_collision).
        """
        x, y = self.level_one.hazard_meteor.get_current_position()
        if y > HEIGHT:
            self.update_collision_position(self.level_one.hazard_meteor.name)

    def screen_collision_rolling_rock(self):
        """
        Rolling rock moves left to right along the ground.
        When it exits the right side of the screen, reset it back to
        the left side so it loops around.
        """
        x, y = self.level_one.hazard_rollingRock.get_current_position()
        if x > WIDTH:
            # Reset to just off the left edge, keep same y (ground level)
            self.level_one.hazard_rollingRock.rect.x = -60
            self.level_one.hazard_rollingRock.rect.y = self.level_one.hazard_rollingRock.position_y

    # THIS REMOVE
    def screen_collision_hazard(self):
        """Checks all hazards for screen-edge resets."""
        self.screen_collision_meteor()
        # THIS REMOVE
        # self.screen_collision_rolling_rock()


    def add_models_collision(self):
        """Register all level-one sprites for collision checking."""
        self.models_collision[self.level_one.character] = self.level_one.character.name
        self.models_collision[self.level_one.hazard_meteor] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorOne] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorTwo] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_rollingRock] = self.level_one.hazard_rollingRock.name

    def reset_level(self):
        # reset character position and game state
        self.level_one.character.rect.center = (self.level_one.character.position_x, self.level_one.character.constant_ground)
        self.level_one.character.game_state = "idle"
        self.level_one.character.speed_y = 0
        self.level_one.character.png_on_ground = True
        # reset hazard positions
        self.level_one.hazard_meteor.update_position_collision()
        self.level_one.hazard_meteorOne.update_position_collision()
        self.level_one.hazard_meteorTwo.update_position_collision()
        self.level_one.hazard_rollingRock.update_position_collision()

        # reset slowdown state so hazards return to normal speed after level reset
        self.slow_hazards_active = False
        self.slow_hazards_timer = 0
        self.restore_hazard_speeds()

    # Collect all hazards in this level so the slowdown effect can be applied uniformly
    # Include dynamically created meteors in the slowdown system
    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_one.hazard_meteor,
            self.level_one.hazard_meteorOne,
            self.level_one.hazard_meteorTwo,
            self.level_one.hazard_rollingRock,
        ]

        # include extra meteors too, if they are active in this level
        for meteor in self.meteors:
            self.slowed_hazards.append(meteor)

    # this is a helper to detect which speed attribute a hazard uses
    # because current hazard classes use "speed" and "move_x"
    def get_hazard_speed_attribute(self, hazard):
        if hasattr(hazard, "speed"):
            return "speed"
        elif hasattr(hazard, "move_x"):
            return "move_x"
        return None
    
    # this function applies the slowdown on the hazards
    # reduces speed of all hazards while storing their original values for later reseting
    def apply_slow_hazards(self):
        for hazard in self.slowed_hazards:
            attr = self.get_hazard_speed_attribute(hazard)
            if attr is None:
                continue

            if hazard not in self.original_hazard_speeds:
                self.original_hazard_speeds[hazard] = getattr(hazard, attr)

            original_speed = self.original_hazard_speeds[hazard]
            slowed_speed = max(1, int(original_speed * self.slow_factor))
            setattr(hazard, attr, slowed_speed)

    # this function resets the speed of the hazards to their original before slowdown
    def restore_hazard_speeds(self):
        for hazard, original_speed in self.original_hazard_speeds.items():
            attr = self.get_hazard_speed_attribute(hazard)
            if attr is not None:
                setattr(hazard, attr, original_speed)


    # spawns a random powerup: 60% shield, 20% time reduction and 20% SlowerHazards
    def spawn_powerup(self):
        temp = random.random()
        if temp < 0.60:
            self.current_powerup = ShieldBubble()
        elif temp < 0.80:
            self.current_powerup = TimeReduction()
        else: 
            self.current_powerup = SlowerHazards()

    # update powerup each frame, handles spawn timer
    def update_powerup(self, delta_time):
        # Tick down the shield timer if active
        character = self.level_one.character
        if getattr(character, 'shield_active', False):
            character.shield_timer -= delta_time
            if character.shield_timer <= 0:
                character.shield_active = False
                character.shield_timer = 0

        # Tick down the slowdown timer if active
        if self.slow_hazards_active:
            self.slow_hazards_timer -= delta_time
            if self.slow_hazards_timer <= 0:
                self.slow_hazards_active = False
                self.slow_hazards_timer = 0
                self.restore_hazard_speeds()

        # If no powerup is active, count up spawn timer
        if self.current_powerup is None or not self.current_powerup.is_active:
            self.powerup_spawn_timer += delta_time
            if self.powerup_spawn_timer >= self.powerup_spawn_interval:
                self.spawn_powerup()
                self.powerup_spawn_timer = 0  # reset timer
        else:
            # Powerup is active, update its position
            self.current_powerup.update_position()

    # check if character collided with powerup
    def detection_collision_powerup(self):
        if self.current_powerup is None or not self.current_powerup.is_active:
            return
        # Use mask collision like hazards
        group = pygame.sprite.Group()
        group.add(self.current_powerup)
        if pygame.sprite.spritecollide(
            self.level_one.character, group, False, pygame.sprite.collide_mask):
            self.current_powerup.apply_effect(self.level_one.character)

            # activate the slowdown effect
            if isinstance(self.current_powerup, SlowerHazards):
                self.slow_hazards_active = True
                self.slow_hazards_timer = 5000
                self.apply_slow_hazards()

            self.time_penalty_ms += self.current_powerup.time_penalty
            self.current_powerup.is_active = False
            self.current_powerup = None
            print("Powerup collected!")
