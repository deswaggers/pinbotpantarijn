# Mode bumpers
import procgame
from procgame import *
import locale
import random
from mystery import *

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
        self.mystery = Mystery(self.game, 20)
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode2)


    def startmode2(self):
        self.game.modes.add(self.mystery)
        self.mystery.start_feature()

    
    def mode_stopped(self):
        self.layer = None

    def stop_mode2_2sec(self):
        self.delay(name='stop_mode2', event_type=None, delay=2, handler=self.stop_mode2)
    def stop_mode2(self):
        self.game.current_player().stop_eject_mode_mode(self)

    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
