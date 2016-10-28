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
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.display_instructions()
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode2)


    def startmode2(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_starwars_cantina_band', loops=-1)

    def update_lamps(self):
        self.game.effects.drive_lamp('score_energy', 'slow')
        self.game.effects.drive_lamp('solar_energy','medium')
    
    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)


    def display_instructions(self):
        self.instruction_layer.set_text('WELKOM')
        self.layer = self.instruction_layer

    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
