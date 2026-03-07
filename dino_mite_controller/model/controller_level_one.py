from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.character_game.Hazard import RollingRock
from dino_mite_model.level_model.levelone import LevelOne

import pygame


class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()
        self.meteors = []        # separate list
        self.rolling_rocks = []  # separate list
        self.models = dict()

    def update_level_one(self):
        for meteor in self.meteors:
            meteor.update_position()
        self.meteors = [m for m in self.meteors if m.is_active]

        for rock in self.rolling_rocks:
            rock.update_position()
        self.rolling_rocks = [r for r in self.rolling_rocks if r.is_active]

    def spawn_meteor(self):
        self.meteors.append(Meteor())

    def spawn_rolling_rock(self):
        self.rolling_rocks.append(RollingRock())
    
    '''
    if frame_count % 60 == 0:   # meteor every 60 frames
        controller.spawn_meteor()

    if frame_count % 120 == 0:  # rock every 120 frames
        controller.spawn_rolling_rock() 
    '''

    def start_level_one (self):
        return self.level_one

    def detection_collision_character(self, sprite, group) -> bool:
        sprites_group = pygame.sprite.Group()
        sprites_group.add(group)  # pass self.meteors or self.rolling_rocks
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



