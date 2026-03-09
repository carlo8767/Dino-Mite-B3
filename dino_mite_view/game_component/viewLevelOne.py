import pygame

from dino_mite_controller.model.controller_level_one import ControllerLevelOne
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelOne:

   dict_elements_view = dict()

   def draw_screen_level_one(self, window, ctr_levelOne):
       print(">> Enter in View Level One")
       # NEED TO PASS THE CONTROLLER
       # c_level_one =  model_level_one
       # FRAME IMAGE
       clock = pygame.time.Clock()
       clock.tick(60)
       # UPLOAD CAPTION
       pygame.display.set_caption(utilities_names.LEVEL_ONE)
       # UPLOAD IMAGE BACKGROUND
       sprite_image_background = pygame.image.load(ctr_levelOne.level_one.image).convert()
       # VERIFY IF CHANGE THE IMAGE
       sprite_image_background = pygame.transform.scale(sprite_image_background, (WIDTH, HEIGHT))

       while True:
         # CREATION UTILITY EVENT
         for event in pygame.event.get():
             pass
         keys = pygame.key.get_pressed()
         # CHARACTER MOVE
         if keys[pygame.K_LEFT]:
             ctr_levelOne.movement_character_left()
         elif keys[pygame.K_RIGHT]:
              ctr_levelOne.movement_character_right()
         window.blit(sprite_image_background, (0, 0))
         # DRAW COMPONENTS
         self.draw_component_levels_one(window, ctr_levelOne)
         # COLLISION RECTANGLE
         collude_ver, name = ctr_levelOne.detection_collision_character(ctr_levelOne.level_one.character)
         if collude_ver:
                 print(f'occuring collision {name}')
                 ctr_levelOne.update_collision_position(name)
         # COLLISION LIMIT
         ctr_levelOne.screen_collision_hazard()
         pygame.display.update()



   def draw_component_levels_one(self, window, ctr_level_one):
     window.blit(ctr_level_one.level_one.hazard_meteor.image_loaded, ctr_level_one.level_one.hazard_meteor.rect)
     # CHANGE HAZARD POSITION PASS THE LOGIC IN THE CONTROLLER?
     ctr_level_one.level_one.hazard_meteor.rect.y += 2
     window.blit(ctr_level_one.level_one.hazard_rollingRock.image_loaded, ctr_level_one.level_one.hazard_rollingRock.rect)
     ctr_level_one.level_one.hazard_rollingRock.rect.y += 2
     window.blit(ctr_level_one.level_one.character.image_loaded, ctr_level_one.level_one.character.rect)
     # VERIFY IF THEY REACH THE LIMIT SCREEN





