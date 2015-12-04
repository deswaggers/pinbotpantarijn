# Mode bumpers
import procgame
from procgame import *
import locale
import random


# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Mode1(game.Mode):

        def __init__(self, game, priority):
                super(Mode1, self).__init__(game, priority)
                

        def mode_started(self):
                ## eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
                self.delay(name='Mode_start_na_eject', event_type=None, delay=2, handler=self.mode_start_na_eject)
                
        def mode_start_na_eject(self):
                self.game.effects.eject_ball('eject')
                self.bumperscore=40
                self.bumperraise=0
                self.time_left=20
                self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)
                self.bumpers_hit()
        def mode_stopped(self):
                self.layer = None
                
## switches
                
        def sw_Ubumper_active(self,sw):
                self.bumpers_hit() 
                return procgame.game.SwitchStop
        def sw_Bbumper_active(self,sw):
                self.bumpers_hit() 
                return procgame.game.SwitchStop
        def sw_Lbumper_active(self,sw):
                self.bumpers_hit()   
                return procgame.game.SwitchStop
        def sw_slingR_active(self,sw):
                self.bumpers_hit() 
                return procgame.game.SwitchStop
        def sw_slingL_active(self,sw):
                self.bumpers_hit() 
                return procgame.game.SwitchStop


## Lampen
        

## Mode functions
        def energyflash(self):
                self.game.coils.Solenoidselect.pulse(90)   
                self.game.coils.RampLow_EnergyFlash.pulse(70)
                     
        def countdown(self):
                self.time_left-=1
                self.shoot_bumpers_animation()
                if self.time_left<1:
                        self.game.modes.remove(self)
                self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)
                
                
        def bumpers_hit(self):
                ## Score-systeem
                #self.energyflash()
                self.bumperraise+=1
                if self.bumperraise>6:
                        self.bumperscore+=20
                        self.bumperraise=0
                self.game.score(self.bumperscore)
                ##geluid
                if self.bumperscore<=60:
                        self.game.sound.play("sound_lasergun1")
                elif self.bumperscore<=100:
                        self.game.sound.play("sound_lasergun2")
                else:
                        self.game.sound.play("sound_lasergun3")
                ## Display
                self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.raise_layer = dmd.TextLayer(5, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.score_layer.set_text("EACH:: " +str(self.bumperscore),True)
                self.raise_layer.set_text("RAISE AT 6:.  ." +str(self.bumperraise)+ 'time left:'+str(self.time_left),True) ## modetimer met healthbar doen?
                x=random.random()
                if x>0.7:
                        self.text_layer.set_text('BAM!',True)
                elif x>0.4:
                        self.text_layer.set_text('WHAM',True)
                else:
                        self.text_layer.set_text('BOOM',True)
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_1.gif') #Als het goed is kan ie ook rechtstreeks gif-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.score_layer, self.raise_layer, self.text_layer])
                self.shoot_bumpers_animation()

        def shoot_bumpers_animation(self):
                #self.text_layer.set_text('aim for the bumpers!',True)
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_2.gif') #Als het goed is kan ie ook rechtstreeks png-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.score_layer, self.raise_layer, self.text_layer])
