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


class Mode5(game.Mode):
    def __init__(self, game, priority):
        super(Mode5, self).__init__(game, priority)

    def mode_started(self):
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.display_instructions()
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode5)
        self.numberHits = 0


    def startmode5(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_harp', loops=-1)


    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)


    def display_instructions(self):
        self.instruction_layer.set_text('First instructions here')
        self.layer = self.instruction_layer

    
    def reset_multiplier(self):
        if self.numberHits>0:
            self.numberHits-=1
            self.game.sound.play("sound_outlane")
            

    def sw_Rbank1_active(self, sw):
        self.numberHits += 1
        self.game.score(1000 * (2**self.numberHits))
        self.delay(name='reset_multiplier', event_type=None, delay=5, handler=self.reset_multiplier)
        self.game.sound.play("sound_hit")

    

    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
