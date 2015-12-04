import procgame
from procgame import *
import locale

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Droptargets(game.Mode):

        ## Mees heeft een nieuwere, dus hieronder nog de oudere versie met alleen de locatieverwijzing aangepast

        def __init__(self, game, priority):
                super(Droptargets, self).__init__(game, priority)
				#Dit hoeft niet meer omdat alle geluiden nu worden geregistreerd in general_play
                #self.game.sound.register_sound('bumper1', sound_path+"lasergun1.wav")
                #self.game.sound.register_sound('bumper2', sound_path+"lasergun2.wav")
                #self.game.sound.register_sound('bumper3', sound_path+"lasergun3.wav")
                

        def mode_started(self):
                self.dropscount=0
                self.game.effects.drive_lamp('drops','medium')

##                self.energyscore=0
##                self.dropscount=0

        def mode_stopped(self):
                pass



        def drops_reset(self):
                self.game.coils.Drops_RightInsBFlash.pulse(120)
                self.dropscount=0
                self.drop_timer = 0
                self.game.effects.drive_lamp('drops','medium')
                print "drops-reset" 
                


        def drops_check(self):
                self.game.effects.drive_lamp('drops','off')
                if self.dropscount==0:
                        self.dropscount=1
                        self.game.score(200)
                        print "eerste droptarget"
                        self.delay(name='drop_timer', event_type=None, delay=6, handler=self.drops_reset)
                        
                        
                elif self.dropscount==1:
                        self.dropscount=2
                        self.game.score(1000)
                        self.delay(name='drop_timer', event_type=None, delay=6, handler=self.drops_reset)
                        print "2e droptarget"

                elif self.dropscount==2:
                        self.game.score(10000)
                        print "3e droptarget"
                        self.cancel_delayed('drop_timer')
                        self.drops_reset()
                self.game.sound.play("sound_lasergun1")
                
## switches
                
        def sw_droptarget1_active_for_200ms(self,sw):
                self.drops_check()

        def sw_droptarget2_active_for_200ms(self,sw):
                self.drops_check()

        def sw_droptarget3_active_for_200ms(self,sw):
                self.drops_check()
        


#### Lampen
##        
##
#### Mode functions
##
##        def check_drops(self, num):
##            self.dropscount+=1
##            self.game.score(10)
##            self.energyflash()
##            self.bumpers_animation()
##            self.delay(name='display_multiball_layer', event_type=None, delay=0.3, handler=self.display_multiball_layer)
##             
##        def energyflash(self):
##             self.game.coils.Solenoidselect.pulse(90)   
##             self.game.coils.RampLow_EnergyFlash.pulse(70)
##
##        
##                     
#### Animations
##                
##        def bumpers_animation(self):
####                pass
##                self.energyscore+=1
##                self.title_layer = dmd.TextLayer(110, 2, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10
##                self.title_layer.set_text(str(self.energyscore),True)  
##                anim = dmd.Animation().load(dmd_path+'yoda.dmd')
##                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
##                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer])
##                self.delay(name='clear_layer', event_type=None, delay=3, handler=self.clear_layer)
##            
##        def clear_layer(self):
##             self.layer = None
