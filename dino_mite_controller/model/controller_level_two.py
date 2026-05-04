from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.leveltwo import LevelTwo
from dino_mite_model.character_game.vertical_hazard import BigArm
import random
import pygame

class ControllerLevelTwo(BaseLevelController):
    """
    Controller for Level 2.

    Hazards: 3 fireballs (vertical) + 1 mammoth leg (vertical stomp).
    
    All four are registered so collision detection, movement, the slowdown
    powerup, and level reset all work automatically.
    """

    def __init__(self):
        self.level_model = LevelTwo()
        self.level_number = 2
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_fireball,
            self.level_model.hazard_fireballOne,
            self.level_model.hazard_fireballTwo,
            self.level_model.hazard_bigArm,
        ]
    def update_movement_hazard(self):

        player1 = self.level_model.character
        player2 = self.level_model.characterTwo

        #two_player_mode = self.get_player_two_status()

        player1_alive = self.get_player_one_status()
        player2_alive = self.get_player_two_status()

        for hazard in self.slowed_hazards:
            if isinstance(hazard, BigArm):
                if player1_alive and player2_alive:
                    hazard.update_position(player_centerx=(player1.rect.centerx, player2.rect.centerx))
                elif player2_alive:
                    hazard.update_position(player_centerx=player2.rect.centerx)
                else:
                    hazard.update_position(player_centerx=player1.rect.centerx)
            else:
                hazard.update_position()

    def _build_deck(self) -> list:
        """One deck = 5 cards: 3 shields, 1 time reduction, 1 slow.
        Shuffled so the order is unpredictable but the 60/20/20 ratio is exact."""
        deck = (
                [self.level_model.pw_up_shield_bubble] * 3 +
                [self.level_model.pw_up_time_reduction] * 1 +
                [self.level_model.pw_up_slower_hazard] * 1
        )
        random.shuffle(deck)
        return deck

    def init_music(self):
        pygame.mixer.music.load(self.level_model.sound)
        pygame.mixer.music.set_volume(self.level_model.sound_volume)
        pygame.mixer.music.play(-1, 0.0)

    def init_music_end_level(self):
        pygame.mixer.music.load(self.level_model.sound_end_game)
        pygame.mixer.music.play(-1, 0.0)