import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dino_mite_view.game_component.frame_game_component_central import FrameGameComponent

if __name__ == '__main__':
    init_games_dino = FrameGameComponent()