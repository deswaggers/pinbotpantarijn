# Mode bumpers
import procgame
from procgame import *
import locale
import random

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path + "sound/speech/"
sound_path = game_path + "sound/fx/"
music_path = game_path + "sound/music/"
dmd_path = game_path + "dmd/"


class Mode2(game.Mode):
        def __init__(self, game, priority):
                super(Mode2, self).__init__(game, priority)
        def mode_started(self):
                self.test_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.display_dinges()
                self.bumpers_hit()

        # Wtf
        def display_dinges(self):
                self.test_layer.set_text('HALLO WERELD!')
                self.layer = self.test_layer
                # dmd.GroupedLayer(128, 32, [self.animation_layer, self.text_layer])
                
        def eject_ball(self):
                self.game.effects.eject_ball('eject')
        #Bumpers         
        def bumpers_hit(self):
                self.game.effects.drive_lamp('advance_planet','on')


