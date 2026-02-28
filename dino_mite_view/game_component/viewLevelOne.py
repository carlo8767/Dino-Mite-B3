import pygame

from dino_mite_utility import utilities_names



class ViewLevelOne:

   def draw_screen_level_one(self, window, model_level_one):
       print(">> Enter in View Level One")
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
             model_level_one.character.rectangle.x -= 2
         if keys[pygame.K_RIGHT]:
              model_level_one.character.rectangle.x += 2
         window.blit(sprite_image_background, (0, 0))
         # UPLOAD IMAGE HAZARD
         window.blit(model_level_one.hazard_level_one.image_loaded, model_level_one.hazard_level_one.rectangle)
         # CHANGE HAZARD POST
         model_level_one.hazard_level_one.rectangle.y +=2
         # UPLOAD IMAGE CHARACTER
         window.blit(model_level_one.character.image_loaded, model_level_one.character.rectangle)
         pygame.display.update()



