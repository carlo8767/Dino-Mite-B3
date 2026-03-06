import pygame

from dino_mite_controller.model.controller_level_one import ControllerLevelOne
from dino_mite_utility import utilities_names



class ViewLevelOne:

   def draw_screen_level_one(self, window, model_level_one):
       print(">> Enter in View Level One")
       # NEED TO PASS THE CONTROLLER
       c_level_one =  ControllerLevelOne()
       # FRAME IMAGE
       clock = pygame.time.Clock()
       clock.tick(60)
       # UPLOAD CAPTION
       pygame.display.set_caption(utilities_names.LEVEL_ONE)
       # UPLOAD IMAGE BACKGROUND
       sprite_image_background = pygame.image.load(model_level_one.image).convert()
       while True:
         # CREATION UTILITY EVENT
         for event in pygame.event.get():
             pass
         keys = pygame.key.get_pressed()
         # CHARACTER MOVE
         if keys[pygame.K_LEFT]:
             model_level_one.character.rect.x -= 2
         if keys[pygame.K_RIGHT]:
              model_level_one.character.rect.x += 2
         window.blit(sprite_image_background, (0, 0))
         # UPLOAD IMAGE HAZARD
         window.blit(model_level_one.hazard_level_one.image_loaded, model_level_one.hazard_level_one.rect)
         # CHANGE HAZARD POST
         model_level_one.hazard_level_one.rect.y +=2
         # UPLOAD IMAGE CHARACTER
         window.blit(model_level_one.character.image_loaded, model_level_one.character.rect)
         # COLLISION RESTART THE HAZARD
         if c_level_one.detection_collision_character(model_level_one.hazard_level_one, model_level_one.character ):
                 model_level_one.hazard_level_one.update_positions(400, 2)
         else:
             # UNDERSTAND HOW TO CREATE MULTIPLE HAZARD AND DETECT MULTIPLE COLLISION
              if  model_level_one.hazard_level_one.rect.x > 800 or   model_level_one.hazard_level_one.rect.y > 800:
                  model_level_one.hazard_level_one.update_positions(400, 2)

         pygame.display.update()




