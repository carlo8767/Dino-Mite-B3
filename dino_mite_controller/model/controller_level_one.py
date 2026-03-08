from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_model.character_game.player_movement import Player_Movement

import pygame


class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()
        self.hazards = []
        self.models = dict()

    def update_level_one(self):
        for hazard in self.hazards:
            hazard.update_position()
        self.hazards = [hazard for hazard in self.hazards if hazard.is_active]

    def spawn_meteor(self):
        self.hazards.append(Meteor())

    def start_level_one (self):
        return self.level_one

    def detection_collision_character(self, sprite, group) -> bool:
        sprites_group = pygame.sprite.Group()
        sprites_group.add(group)
        # IF COLLUDE RESTART THE LEVEL !!
        if pygame.sprite.spritecollide(sprite, sprites_group, True):
            print("collude")
            return True
        """"
        https://www.pygame.org/docs/tut/SpriteIntro.html
        """

    def movement_character_left(self):
        if self.screen_collision_character("L"):
            x, y = self.level_one.character.get_current_position()
            self.level_one.character.set_current_position(x,y)
        else:
            self.level_one.character.movement_character_left()

    def movement_character_right(self):
        if self.screen_collision_character("R"):
            print("SCRREN")
            x, y = self.level_one.character.get_current_position()
            print(x)
            self.level_one.character.set_current_position(x,y)
        else:
            self.level_one.character.movement_character_right()

    def update_collision_position_hazard(self):
       self.level_one.hazard_level_one.update_position_collision()


    def screen_collision_hazard(self):
        x, y = self.level_one.hazard_level_one.get_current_position()
        if self.level_one.verification_limit_screen_colision(x,y):
            self.update_collision_position_hazard()

    def screen_collision_character(self, verse_x):
        x, y = self.level_one.character.get_current_position()
        return self.level_one.verification_limit_screen_colision(x,y, verse_x)


    # JUST ADD MODELS COMPONENT LEVELS ONE
    def add_models(self):
        self.models[self.level_one.hazard_level_one.name] = self.level_one.hazard_level_one
        self.models[self.level_one.character.name] = self.level_one.character

    # ADDED: forwards keys and events down to player_movement in the model
    def handle_player_input(self, keys, events):
        self.level_one.character.player_movement.handle_key_input(keys, events)

    # ADDED: forwards gravity call down to player_movement in the model
    def apply_player_gravity(self):
        self.level_one.character.player_movement.gravity()

    # ADDED: forwards draw call down to player_movement which picks the correct image
    def draw_character(self, window):
        self.level_one.character.player_movement.draw(window)



