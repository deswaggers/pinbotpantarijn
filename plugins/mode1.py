import procgame
from procgame import *
import locale

# all paths
game_path = "C:\P-ROC\pyprocgame-master\games\VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Mode1(game.Mode):
        def __init__(self, game, priority):
            super(Mode1, self).__init__(game, priority)

            self.score_layer = dmd.TextLayer(125, 6, self.game.fonts['num_14x10'], "right", opaque=False)
            self.value_layer = dmd.TextLayer(126, 22, self.game.fonts['tiny7'], "right", opaque=False) #07x5

##            self.game.lampctrl.register_show('mode1_lampshow', lampshow_path +"planeten_short.lampshow")

            self.mode1_score = 0
            self.hurryup_value=50000


        def mode_started(self):
            print("Debug, Mode1 Started")
            # start mode1 intro
            self.mode1_intro()
            self.display_mode1_layer()
            self.game.sound.fadeout_music(time_ms=2800)

        def mode_stopped(self):
            self.game.current_player().mode_running = 0
            print("Debug, Mode1 Stopped")

## lamps & animations

        def update_lamps(self):
            self.game.effects.energy_flash(45000/217/10)


        def display_mode1_layer(self):
             p = self.game.current_player()
             scoreString = locale.format("%d",p.score, True)
             self.score_layer.set_text(scoreString,blink_frames=4)
             self.value_layer.set_text(" HURRY: "+str(locale.format("%d", self.hurryup_value, True)))
             self.layer = dmd.GroupedLayer(128, 32, [self.value_layer, self.score_layer])
             self.delay(name='display_mode1_layer', event_type=None, delay=0.1, handler=self.display_mode1_layer)

        def clear_layer(self):
            self.layer = None


## mode functions

        def mode1_intro(self):
            #self.game.sound.play()
            self.game.effects.gi_blinking(cycle_seconds=1)

            #play lightshow
##            self.game.lampctrl.play_show('mode1_lampshow', True, 'None')
            # delay multiballstart to wait for end of lampshow and perhaps animation
            self.delay(name='start_mode', event_type=None, delay=0.5, handler=self.start_mode_1)

        def start_mode_1(self):

             #stop lightshow
             self.game.lampctrl.stop_show()

             #play music
             self.game.sound.play_music('music_mario_invincible')

             #update lamps for entire game after lampshow
             self.delay(name='update_lamps', event_type=None, delay=0.05, handler=self.update_lamps)

             # eject balls and close visor
             #self.game.coils.Ejecthole_LeftInsBFlash.pulse(40)
             self.yoda_animation = Yoda_animation(self.game, 86)
             self.game.modes.add(self.yoda_animation)

             self.hurryup_countdown()


        def hurryup_countdown(self):
             # repeat call to itself to countdown hurryup value
             if self.hurryup_value > 5000:
                 print self.hurryup_value
                 self.hurryup_value -= 217
                 self.delay(name='hurryup_countdown', event_type=None, delay=0.1, handler=self.hurryup_countdown)
                 #self.hurryup_layer.set_text(locale.format("%d", self.hurryup_value, True))
             else:
                 #self.game.sound.play()
                 self.end_mode1()

## switches
        def sw_Ubumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop
        def sw_Lbumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop
        def sw_Bbumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def bumper(self):
            print ("score hurryup!")
            #self.game.sound.play()
            self.game.score(self.hurryup_value)
            self.cancel_delayed('hurryup_countdown')
            self.end_mode1()

        def end_mode1(self):
             print ("clear hurryup!")
             self.game.modes.remove(self.yoda_animation)
             self.game.coils.RampLow_EnergyFlash.disable()
             self.game.coils.Solenoidselect.disable()
             # stop hurryup music
             self.game.sound.stop_music()
             # cancel delays in case its running
             self.cancel_delayed('hurryup_countdown')
             self.game.sound.play_music('music_starwars_theme')
             # restart main theme music
             self.hurryup_value=50000
             # remove from mode qeue
             self.game.modes.remove(self)


        # check whether allscoresdouble or end mode when a ball drains
        def sw_outhole_active(self,sw):
            print('number balls in play=', self.game.trough.num_balls_in_play)
            self.game.coils.outhole_knocker.pulse(30)
            self.end_mode1()
            return procgame.game.SwitchStop

class Yoda_animation(game.Mode):
        def __init__(self, game, priority):
                super(Yoda_animation, self).__init__(game, priority)
        def mode_started(self):
                self.start_yoda_animation()

        def start_yoda_animation(self):
                anim = dmd.Animation().load(dmd_path+'yoda.dmd')
                self.animation_yoda_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=2)
                self.layer = self.animation_yoda_layer
                self.layer.composite_op = "blacksrc" #blacksrc
