# Mode bumpers
import procgame
from procgame import *
import locale
import random
import webbrowser

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path + "sound/speech/"
sound_path = game_path + "sound/fx/"
music_path = game_path + "sound/music/"
dmd_path = game_path + "dmd/"


class Mode4(game.Mode):
    def __init__(self, game, priority):
        super(Mode4, self).__init__(game, priority)

    def mode_started(self):
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_07x4'], opaque=False)
        self.timer_layer = dmd.TextLayer(8, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)

        self.display_instructions()
        self.delay(name='start_mode2', event_type=None, delay=2, handler=self.startmode2)
        self.rampCount=0
        self.game.sound.play("sound_2017_houston_we_got")
        img = "images_for_beamer/shoot_ramp.png"
        webbrowser.open(img)        

    def startmode2(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_starwars_imperialmarch', loops=-1)
        self.flash_upper()
        

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


    def sw_rampexit_active(self, sw):
        self.rampCount+=1
        self.game.score(2000*(self.rampCount*self.rampCount))
        
        if self.rampCount==1:
            self.time_left=24
            self.game.sound.play("sound_2017_biem")
            self.countdown()
        elif self.rampCount==2:          
            self.game.sound.play("sound_2017_biem")
        elif self.rampCount==3:
            self.game.sound.play("sound_2017_explosie") 
            self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop

    def countdown(self): 
        self.time_left-=1
        # Roep de functie shoot_bumpers_animation aan. Dit doet ie dus elke seconde. Ook even de flasher bij de pop-bumpers flashen
        self.showTime()
        if self.time_left<6:
            self.game.sound.play("sound_2017_nuke_alarm")
        elif self.time_left<1:
            self.endmode()
        # elke seconde wordt countdown weer gestart
        self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)


    def flash_upper(self):
        self.game.effects.upperPlayfield_flash()
        self.game.effects.leftPlayfield_flash()
        self.delay(name='flashramps', event_type=None, delay=1, handler=self.flash_upper)
        
            
        
    def endmode(self):
        self.game.current_player().stop_eject_mode_mode(self)

    def showTime(self):
        self.timer_layer.set_text('TIME LEFT: '+ str(self.time_left),True)
        anim = dmd.Animation().load(dmd_path+'life_bar.dmd') # Een dmd bestand bestaat uit frames van plaatjes die zijn omgezet in iets leesbaars voor PROCGAME
        self.lifebar_layer = dmd.FrameLayer(opaque=True, frame = anim.frames[24-self.time_left])
        self.lifebar_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.lifebar_layer,self.timer_layer])
        


