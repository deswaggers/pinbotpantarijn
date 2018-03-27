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


class RampMultiball(game.Mode):
    def __init__(self, game, priority):
        super(RampMultiball, self).__init__(game, priority)

    def mode_started(self):
        print "RampMultiball uit ramp_multiball.py is gestart"
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.game.lampctrl.register_show('multiball_start', lampshow_path +"planeten_short.lampshow")
        self.game.lampctrl.register_show('visor_lampshow', lampshow_path +"Pinbot_1.lampshow")
        self.delay(name='start_rampMB', event_type=None, delay=5, handler=self.start_rampMB)
        self.display_instructions()


    def start_rampMB(self):
        self.game.start_ball()
        self.game.sound.play_music('music_harp', loops=-1)


    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)


    def display_instructions(self):
        self.instruction_layer.set_text('First instructions here')
        self.layer = self.instruction_layer


    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
