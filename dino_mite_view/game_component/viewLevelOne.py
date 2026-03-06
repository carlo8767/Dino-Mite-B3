import pygame

from dino_mite_controller.model.controller_level_one import ControllerLevelOne
from dino_mite_utility import utilities_names



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
         # UPLOAD IMAGE HAZARD
         window.blit(ctr_levelOne.level_one.hazard_level_one.image_loaded, ctr_levelOne.level_one.hazard_level_one.rect)
         # CHANGE HAZARD POST
         ctr_levelOne.level_one.hazard_level_one.rect.y +=2
         # UPLOAD IMAGE CHARACTER
         window.blit(ctr_levelOne.level_one.character.image_loaded, ctr_levelOne.level_one.character.rect)
         # COLLISION RESTART THE HAZARD
         if ctr_levelOne.detection_collision_character(ctr_levelOne.level_one.character, ctr_levelOne.level_one.hazard_level_one):
                 print("collision")
                 ctr_levelOne.update_collision_position_hazard ()

         # DETECTION COLLISION
         ctr_levelOne.screen_collision_hazard()





         # else:
             # UNDERSTAND HOW TO CREATE MULTIPLE HAZARD AND DETECT MULTIPLE COLLISION
            #  if  model_level_one.hazard_level_one.rect.x > 800 or   model_level_one.hazard_level_one.rect.y > 800:
             #     model_level_one.hazard_level_one.update_positions(400, 2)
         pygame.display.update()





