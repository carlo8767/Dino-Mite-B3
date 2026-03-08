import pygame

from dino_mite_controller.model.controller_level_one import ControllerLevelOne
from dino_mite_utility import utilities_names



class ViewLevelOne:

   dict_elements_view = dict()

   def draw_screen_level_one(self, window, ctr_levelOne):
       print(">> Enter in View Level One")
       clock = pygame.time.Clock()
       clock.tick(60)
       pygame.display.set_caption(utilities_names.LEVEL_ONE)
       sprite_image_background = pygame.image.load(ctr_levelOne.level_one.image).convert()

       while True:
         # CREATION UTILITY EVENT
         # stored events instead of throwing them away
         events = pygame.event.get()

         keys = pygame.key.get_pressed()

         # CHARACTER MOVE
         # replaced LEFT/RIGHT checks, view just passes inputs to controller
         ctr_levelOne.handle_player_input(keys, events)
         # added gravity call, controller handles the logic
         ctr_levelOne.apply_player_gravity()

         window.blit(sprite_image_background, (0, 0))
         # UPLOAD IMAGE HAZARD
         window.blit(ctr_levelOne.level_one.hazard_level_one.image_loaded, ctr_levelOne.level_one.hazard_level_one.rect)
         # CHANGE HAZARD POST
         ctr_levelOne.level_one.hazard_level_one.rect.y += 2
         # UPLOAD IMAGE CHARACTER
         # replaced static blit, controller draws correct state image
         ctr_levelOne.draw_character(window)
         # COLLISION RESTART THE HAZARD
         if ctr_levelOne.detection_collision_character(ctr_levelOne.level_one.character, ctr_levelOne.level_one.hazard_level_one):
                 print("collision")
                 ctr_levelOne.update_collision_position_hazard()

         # DETECTION COLLISION
         ctr_levelOne.screen_collision_hazard()

         pygame.display.update()