import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dino_mite_view.game_component.game_state_interactor import GameStateInteractor



if __name__ == '__main__':
    init_games_dino = GameStateInteractor()
    init_games_dino.init_game()