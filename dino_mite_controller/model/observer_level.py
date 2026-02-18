from skimage.filters import window

from dino_mite_model.level_model.levelone import LevelOne

import pygame


class Obsever_Levels:



    def receive_notification_level_one_init (self):
        init = LevelOne()
        # TEMPORARY
        init.creation_level_one()

        # call level one
