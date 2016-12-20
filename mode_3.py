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
        self.timer_layer = dmd.TextLayer(8, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.hit_layer = dmd.TextLayer(8, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.score_layer = dmd.TextLayer(20, 40, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.balingat=0
        self.modeScore=420000
        self.schepenkapot = 0
        self.time_left=48
        self.update_lamps()
        self.countdown()
        
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
        self.health=24
        self.cancel_delayed('Mode_countdown')
        if self.schepenkapot==0:
            self.delay(name='tijd', event_type=None, delay=8, handler=self.endTime)
        elif self.schepenkapot==1:
            self.delay(name='tijd', event_type=None, delay=6, handler=self.endTime)
        elif self.schepenkapot==2:
            self.delay(name='tijd', event_type=None, delay=4, handler=self.endTime)
        return procgame.game.SwitchStop

    def endTime(self):
        if self.health <=0:
            self.game.sound.play("sound_2017_biem")
            #moet nog veranderd worden
            self.schepenkapot += 1
            self.game.score(self.modeScore*self.schepenkapot)
        else:
            self.game.sound.play("sound_outlane")
            #moet nog veranderd worden
        if self.schepenkapot>2:
            self.endmode()
        else:
            self.countdown()
        self.game.effects.eject_ball('eject')

    def sw_flipperLwL_active(self,sw):
        if self.balingat == 1:
            self.health-=1

    def sw_flipperLwR(self,sw):
        if self.balingat == 1:
            self.health-=1

    def countdown(self):
        self.time_left-=1
        if self.time_left<1:
            self.update_lamps()
            self.endmode #weet nog niet welke van deze goed is
        self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)
        self.showTime()


    def showTime(self):
        self.timer_layer.set_text('TIME LEFT: '+ str(self.time_left),True)
        anim = dmd.Animation().load(dmd_path+'life_bar.dmd') # Een dmd bestand bestaat uit frames van plaatjes die zijn omgezet in iets leesbaars voor PROCGAME
        self.lifebar_layer = dmd.FrameLayer(opaque=True, frame = anim.frames[24-(self.time_left/2)])
        self.lifebar_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.lifebar_layer,self.timer_layer])

    def showHits(self):
        self.hit_layer.set_text('NUMBER OF HITS: '+ str(self.health),True)
        self.score_layer.set_text('COMPLETE FOR: '+ str(self.modeScore*(self.schepenkapot+1)),True)
        anim = dmd.Animation().load(dmd_path+'life_bar.dmd') # Een dmd bestand bestaat uit frames van plaatjes die zijn omgezet in iets leesbaars voor PROCGAME
        self.hit_layer = dmd.FrameLayer(opaque=True, frame = anim.frames[24-self.health])
        self.hit_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.lifebar_layer,self.hit_layer])
            
    def endmode(self):
        self.game.current_player().stop_eject_mode_mode(self)

    def update_lamps(self):
        self.game.effects.drive_lamp('eject1','slow')
        self.game.effects.drive_lamp('eject2','medium')
        self.game.effects.drive_lamp('eject3','fast')
        if self.time_left<1:
            self.game.lamps['eject1'].disable()
            self.game.lamps['eject2'].disable()
            self.game.lamps['eject3'].disable()
            


        
        
