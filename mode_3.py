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
        self.delay(name='start_mode3', event_type=None, delay=2, handler=self.startmode3)
        self.balingat=0
        self.schepenkapot = 0
        
    def startmode3(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_starwars_cantina_band', loops=-1)
        
    def mode_stopped(self):
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

    def sw_rampexit_active(self, sw):
        #dit is gwn een random geluid en licht, kan nog veranderd worden
        self.game.sound.play("sound_hand-clap-echo")
        self.game.effects.drive_lamp('score_energy','slow')

    def sw_eject_active(self, sw):
        return procgame.game.SwitchStop

    def sw_eject_active_for_500ms(self, sw):
        self.balingat=1
        self.health=30
        if self.schepenkapot==0:
            self.delay(name='tijd', event_type=None, delay=10, handler=self.endTime)
        elif self.schepenkapot==1:
            self.delay(name='tijd', event_type=None, delay=10, handler=self.endTime)
        elif self.schepenkapot==2:
            self.delay(name='tijd', event_type=None, delay=10, handler=self.endTime)
        return procgame.game.SwitchStop

    def endTime(self):
        if self.health <=0:
            self.game.sound.play("sound_2017_biem")
            #moet nog veranderd worden
            self.schepenkapot += 1
            self.game.score(420000*self.schepenkapot)
        else:
            self.game.sound.play("sound_outlane")
            #moet nog veranderd worden
        self.game.effects.eject_ball('eject')
        if self.schepenkapot>2:
            self.endmode()

    def sw_flipperLwL_active(self,sw):
        if self.balingat == 1:
            self.health-=1

    def sw_flipperLwR(self,sw):
        if self.balingat == 1:
            self.health-=1

    def endmode(self):
        self.game.current_player().stop_eject_mode_mode(self)



        
        
