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


class Mode3(game.Mode):
    def __init__(self, game, priority):
        super(Mode3, self).__init__(game, priority)

    def mode_started(self):
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.display_instructions()
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode2)

    def startmode3(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_starwars_cantina_band', loops=-1)
        balingat=0
        health=75

    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

    def sw_rampexit_active(self, sw):
        #dit is gwn een random geluid en licht, kan nog veranderd worden
        self.game.sound.play("sound_hand-clap-echo")
        self.game.effects.drive_lamp('score_energy','slow')


'''
    def sw_flipperLwL_active
        if balingat = 1:
            health-=1

    def sw_flipperLwR
        if balingat = 1:
            health-=1

    def 
'''


        
        
