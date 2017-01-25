# Effects
#
# Basic mode for general effects and control of game items (lamps, coils, etc.)

import procgame
import locale
from procgame import *
import time

game_path = game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Animations(game.Mode):

    def __init__(self, game):
        super(Animations, self).__init__(game, 4)
        self.game.sound.register_sound('ramp_up', sound_path+"rampup.wav")