# Bumpers

from procgame import *
import locale

# all paths
game_path = "C:\P-ROC\pyprocgame-master\games\VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Bumpers(game.Mode):

        def __init__(self, game, priority):
                super(Bumpers, self).__init__(game, priority)
				#Dit hoeft niet meer omdat alle geluiden nu worden geregistreerd in general_play
                #self.game.sound.register_sound('bumper1', sound_path+"lasergun1.wav")
                #self.game.sound.register_sound('bumper2', sound_path+"lasergun2.wav")
                #self.game.sound.register_sound('bumper3', sound_path+"lasergun3.wav")
                

        def mode_started(self):
                self.energyscore=0

        def mode_stopped(self):
                pass

                
## switches
                
        def sw_Ubumper_active(self,sw):
             self.game.sound.play("sound_lasergun1")
             self.game.score(10)
             self.energyflash()
             self.bumpers_animation() 

        def sw_Bbumper_active(self,sw):
             self.game.sound.play("sound_lasergun3")
             self.game.score(10)
             self.energyflash()
             self.bumpers_animation() 

        def sw_Lbumper_active(self,sw):
             self.game.sound.play("sound_lasergun2")
             self.game.score(10)
             self.energyflash()
             self.bumpers_animation()   
        



## Lampen
        

## Mode functions
        def energyflash(self):
             self.game.coils.Solenoidselect.pulse(90)   
             self.game.coils.RampLow_EnergyFlash.pulse(70)
                     
## Animations
                
        def bumpers_animation(self):
##                pass
                self.energyscore+=1
                self.title_layer = dmd.TextLayer(110, 2, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10
                self.title_layer.set_text(str(self.energyscore),True)  
                anim = dmd.Animation().load(dmd_path+'yoda.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer])
                self.delay(name='clear_layer', event_type=None, delay=3, handler=self.clear_layer)
            
        def clear_layer(self):
             self.layer = None
