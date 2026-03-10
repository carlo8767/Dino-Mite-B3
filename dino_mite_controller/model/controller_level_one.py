from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.character_game.Hazard import RollingRock
from dino_mite_model.level_model.levelone import LevelOne


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

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def update_movement_level_one(self):
        # Update the single model hazards (the ones actually drawn on screen)
        self.level_one.hazard_meteor.update_position()
        # Update list-based meteors
        for meteor in self.meteors:
            meteor.update_position()

        self.level_one.hazard_rollingRock.update_position()
        # Update list-based rolling rocks, remove when off-screen
        # for rock in self.rolling_rocks:
          #  rock.update_position()
        # self.rolling_rocks = [r for r in self.rolling_rocks if r.is_active]

    def spawn_meteor(self):
        self.meteors.append(Meteor())

    def spawn_rolling_rock(self):
        self.rolling_rocks.append(RollingRock())






        return self.level_one

    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        for g, v in self.models_collision.items():
            # Skip the sprite we are testing (the character itself)
            if g == sprite:
                continue
            sprites_group = pygame.sprite.Group()
            sprites_group.add(g)
            # spritecollide returns a list of colliding sprites
            if pygame.sprite.spritecollide(sprite, sprites_group, True):
                print("collude")
                sprites_group.remove(g)
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
        self.models_collision[self.level_one.hazard_rollingRock] = self.level_one.hazard_rollingRock.name