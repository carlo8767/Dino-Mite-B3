import os

from dino_mite_model.character_game.Hazard import Meteor


class LevelOne:


    def __init__(self):
        self.width = 0
        self.eight = 0
        self.hazard_level_one = Meteor()
        # verify how to pass the absolute path
        self.image = os.path.join('./image', 'backgroundLevelOne.jpeg')
    def creation_level_one(self):
        # VERIFY HOW TO KEEP UPDATE THE VIEW WITHOUT LOOP
        # DRAW HAZARD  AND OTHER COMPONENTS!!
        # UPDATE THE VIEW WHEN ITS FINISH
        levelOne = LevelOne()


        return  levelOne













if  __name__ ==  '__main__':

    s  = LevelOne()

