# Mode bumpers
import procgame
from procgame import *
import random


# All paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Mode1(game.Mode):

        def __init__(self, game, priority):
                super(Mode1, self).__init__(game, priority)

        def mode_started(self):
                self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.raise_layer = dmd.TextLayer(8, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.text_layer = dmd.TextLayer(8, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.update_lamps()
                # eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
                self.delay(name='Mode_start_na_eject', event_type=None, delay=2, handler=self.mode_start_na_eject)

        def mode_start_na_eject(self):
                self.game.effects.eject_ball('eject')
                self.game.sound.play_music('music_harp', loops=-1)
                self.bumperscore=40
                self.bumperraise=0
                self.time_left=25
                self.totalscore=0
                self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)
                self.bumpers_hit()
                self.shoot_message=True

        def mode_stopped(self):
                self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
                self.layer = None

# Switches

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

        def sw_rampexit_active(self, sw): # Ramp zorgt voor extra tijd
                self.time_left+=5
                if self.time_left>25:
                        self.time_left=25
                self.text_layer.set_text("EXTRA 5 SECONDS, " +str(self.time_left)+ "LEFT",True)
                self.layer = dmd.GroupedLayer(128, 32, [self.text_layer])
                self.game.sound.play("sound_hand-clap-echo")

# Als de bal draint tijdens de mode:
        def sw_outhole_active(self, sw):
                self.displaytotalscore()
                return procgame.game.SwitchStop


# Lampen
        def update_lamps(self):
                self.game.effects.drive_lamp('score_energy','fast')
                self.game.effects.drive_lamp('solar_energy','medium')
                # 'tijdbalk' voor hoeveel tijd je nog hebt bij elke getimede mode: planeten van allemaal aan (bovenste knipperen) tot
                # pluto, dan voorbij als pluto uit gaat? Bij sluiten mode moet dan de 'oude staat' van het gewone spel hersteld worden.



# Mode functions
        def energyflash(self):
                self.game.coils.Solenoidselect.pulse(90)
                self.game.coils.RampLow_EnergyFlash.pulse(70)

        def countdown(self):
                self.time_left-=1
                if self.shoot_message==True:
                        self.shoot_message=False
                else:
                        self.shoot_message=True
                self.shoot_bumpers_animation()
                if self.time_left<1:
                        self.displaytotalscore()
                self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)
                self.update_lamps()

        def displaytotalscore(self):
                self.text_layer.set_text('TOTAL SCORE '+str(self.totalscore),True)
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_2.gif') #Als het goed is kan ie ook rechtstreeks png-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.text_layer])
                self.delay(name='End_mode', event_type=None, delay=1.4, handler=self.endmode)
                self.game.sound.fadeout_music(1200)
                self.game.effects.drive_lamp('score_energy','off')
                self.game.effects.drive_lamp('solar_energy','off')
        def endmode(self):
                self.game.current_player().stop_eject_mode_mode(self)

        def bumpers_hit(self):
                # Score-systeem
                self.bumperraise+=1
                if self.bumperraise>6:
                        self.bumperscore+=20
                        self.bumperraise=0
                self.game.score(self.bumperscore)
                self.totalscore+=self.bumperscore
                # Sound
                if self.bumperscore<=60:
                        self.game.sound.play("sound_lasergun1")
                elif self.bumperscore<=100:
                        self.game.sound.play("sound_lasergun2")
                else:
                        self.game.sound.play("sound_lasergun3")
                #  Display
                self.score_layer.set_text("EACH  " +str(self.bumperscore),True)
                self.raise_layer.set_text("RAISE AT 6  " +str(self.bumperraise),True) ## modetimer met healthbar/tijdbalk doen?
                x=random.random()
                if x>0.7:
                        self.text_layer.set_text('BAM!',True)
                elif x>0.4:
                        self.text_layer.set_text('WHAM',True)
                else:
                        self.text_layer.set_text('BOOM',True)
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_1.gif') #Als het goed is kan ie ook rechtstreeks gif-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                anim = dmd.Animation().load(dmd_path+'life_bar.dmd') #Als het goed is kan ie ook rechtstreeks gif-bestanden aan
                self.lifebar_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=0)
                self.lifebar_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.lifebar_layer,self.score_layer, self.raise_layer, self.text_layer])

        def shoot_bumpers_animation(self):
                if self.shoot_message==True:
                        self.text_layer.set_text('SHOOT THE BUMPERS',True)
                else:
                        self.text_layer.set_text('SHOOT THE RAMP',True)
                self.score_layer.set_text("EACH:: " +str(self.bumperscore),True)
                self.raise_layer.set_text("RAISE AT 6: . " +str(self.bumperraise),True) ## modetimer met healthbar/tijdbalk doen?
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_2.gif') #Als het goed is kan ie ook rechtstreeks png-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                anim = dmd.Animation().load(dmd_path+'life_bar.dmd') #Als het goed is kan ie ook rechtstreeks gif-bestanden aan
                self.lifebar_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=0)
                self.lifebar_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.lifebar_layer, self.score_layer, self.raise_layer, self.text_layer])
