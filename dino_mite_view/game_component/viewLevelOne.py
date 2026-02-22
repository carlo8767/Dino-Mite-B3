import pygame


class ViewLevelOne:


    RUN_LEVEL_ONE = True





    # VERIFY IF TURN AROUND
    def draw_window_level_one(self, window, level_one):
         clock = pygame.time.Clock()
         sprite_image_background = pygame.image.load(level_one.image).convert().convert_alpha()
         # WE CAN AS WELL REZISE TRANSFORM SCALE
         sprite_image_hazard = pygame.image.load(level_one.hazard_level_one.image_meteor).convert()
         rectangle_hazard = sprite_image_hazard.get_rect()
         # SET ALPHA

         pygame.display.set_caption("LEVEL ONE")
         y =level_one.hazard_level_one.speed
         while True:
             clock.tick(60)
             # RECTANGLE THIS
             window.blit(sprite_image_background, (0, 0))
             # DRAW HAZARD
             # pygame.draw.rect(window, (0,255,255), rectangle_hazard)
             # DRAW IMAGE MOVE RECTANGLE
             window.blit(sprite_image_hazard, rectangle_hazard)
             y+=2
             rectangle_hazard.topleft =(400,y)
             window.blit(sprite_image_hazard, rectangle_hazard)

             pygame.display.update()
             if y > 800:
                 y = level_one.hazard_level_one.speed








