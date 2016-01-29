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
        self.time_left = 20
        self.test_layer = dmd.TextLayer(0, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.display_instructions()
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode2)
        self.bumpers_hit()
        self.game.current_player().ramp_status_up = True

    def startmode2(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_starwars_cantina_band', loops=-1)
        self.game.current_player().set_mode_running(False)
        self.delay(name='timeleft', event_type=None, delay=1, handler=self.time_reduced)

    def time_reduced(self):
        self.instruction_layer.set_text('Time left: ' + str(self.time_left))
        self.layer = self.instruction_layer

        self.time_left -= 1
        if self.time_left == 0:
            self.game.current_player().stop_eject_mode_mode(self)
        else:
            self.delay(name='timeleft', event_type=None, delay=1, handler=self.time_reduced)

    def bumpers_hit(self):
        self.game.effects.drive_lamp('advance_planet', 'on')

    def mode_stopped(self):
        self.game.current_player().ramp_status_up = False
        self.layer = None

    def display_instructions(self):
        self.instruction_layer.set_text('Hit the thingy below the ramp')
        self.layer = self.instruction_layer
