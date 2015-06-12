#
# Kickstart King mode
#
# Main game mode (1 of 4)
# 2-ball multiball
# Colect nr. of slingshotskicks to lite Jackpot
#

__author__="Pieter"
__date__ ="$21 Jan 2013 21:21:21 PM$"

from procgame import *
import locale
from random import *
import random

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Kickstartking(game.Mode):

        def __init__(self, game, priority):
             super(Kickstartking, self).__init__(game, priority)

             self.game.sound.register_sound('bumper', sound_path+"bumpers.aiff")
             self.game.sound.register_sound('spark', sound_path+"sparkR.ogg")
             self.game.sound.register_sound('jackpot', sound_path+"siren.ogg")   # yeahhhhhh, hail to the king baby! , Who's youre king? , That sure was some kicking! , Kick ass man! Kick ass!
             self.game.sound.register_sound('jackpot_missed', sound_path+"jackpot_missed.ogg")

             self.game.sound.register_sound('jackpot_lit', speech_path+"jackpotislit.wav")
             self.game.sound.register_sound('kick', speech_path+"kick.wav")  #oohmpfff, kick!, yeah, humm
             self.game.sound.register_sound('kick_hurryup', speech_path+"extra_ball_hurryup.wav")

             self.game.sound.register_music('kickstartking_theme', music_path+"kickstartking.ogg")

             self.game.lampctrl.register_show('mode_jackpot', lampshow_path+"mode_jackpot.lampshow")
             self.game.lampctrl.register_show('sling_left', lampshow_path+"sling_left.lampshow")
             self.game.lampctrl.register_show('sling_right', lampshow_path+"sling_right.lampshow")

             self.title_layer = dmd.TextLayer(100, 3, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10
             self.kicks_layer = dmd.TextLayer(100, 13, self.game.fonts['num_14x10'], "center", opaque=False)
             self.value_layer = dmd.TextLayer(100, 27, self.game.fonts['tiny7'], "center", opaque=False)
             self.score_layer = dmd.TextLayer(128/2, 17, self.game.fonts['num_14x10'], "center", opaque=False)

             self.roadkingslamps = ['targetR','targetO','targetA','targetD','targetK','targetI','targetN','targetG','targetS']
             self.slingshotlamps = ['bonus2x','bonus3x','bonus4x','bonus5x','bonus20k','bonus40k','bonus60k','bonus80k']

             self.index = len(self.roadkingslamps)
             self.temp_list = []
             self.target_timer = 3 #VIA MENU
             self.kicks_setting = 4 #VIA MENU
             self.kicks_score = 50000
             self.jackpot_value = 5161610
             self.lite_jackpot = False
             self.kickstartking_score = 0

        def mode_started(self):
             print("Debug, Kickstartking Mode Started")
             self.game.trough.launch_balls(1)
             self.reset_kicks()
             for lamp in self.game.lamps:
                  lamp.disable()

        def mode_stopped(self):
             print("Debug, Kickstartking Mode Stopped")
             self.game.update_lamps()

## lamps & animations

        def update_lamps(self):
             for i in range(len(self.slingshotlamps)):
                 self.game.effects.drive_lamp(self.slingshotlamps[i],'superfast')
             #update kickback lamp
             self.game.base_game_mode.kickback.update_lamps()

        def clear_lamps(self):
             for i in range(len(self.roadkingslamps)):
                 self.game.effects.drive_lamp(self.roadkingslamps[i],'off')
             for i in range(len(self.slingshotlamps)):
                 self.game.effects.drive_lamp(self.slingshotlamps[i],'off')

        def bgnd_animation(self):
             self.bgnd_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'kicks_bgnd.dmd').frames[0])
             self.layer = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.title_layer, self.kicks_layer, self.value_layer])

        def play_animation(self):
               anim = dmd.Animation().load(dmd_path+'bumpers.dmd')
               self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=8)
               self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.kicks_layer, self.value_layer])

        def animation_ended(self):
            self.animation_status = 'ready'
            self.layer = None

        def clear_layer(self):
             self.layer = None

        def lamp_off(self):
             self.game.effects.drive_lamp(self.temp_list[self.index],'off')

## mode functions

        def reset_kicks(self):
             # reset to starting point
             self.lite_jackpot = False
             self.kicks_setting = 4 #VIA MENU
             # set display values
             self.title_layer.set_text('KICKS')
             self.kicks_layer.set_text(str(self.kicks_setting))
             self.value_layer.set_text(str(self.kicks_score))
             # shuffle for next jackpot order
             self.shuffle_jackpot()
             # reset index
             self.index = len(self.roadkingslamps)
             # play background animation
             self.bgnd_animation()
             # update lightning
             self.update_lamps()
             self.game.effects.gi_on()

        def shuffle_jackpot(self):
             # make copy of list to shuffle list for random jackpot target
             self.temp_list = list(self.roadkingslamps)
             shuffle(self.temp_list)
             print(self.temp_list)

        def lit_jackpot(self):
             # repeat call to itself to lite random jackpot
             if self.index > 0:
                 self.index -= 1
                 print(self.index)
                 self.game.sound.play('spark')
                 # light jackpot lamp
                 self.game.effects.drive_lamp(self.temp_list[self.index],'medium')
                 self.delay(name='lit_jackpot', event_type=None, delay=self.target_timer, handler=self.lit_jackpot)
                 # jackpot lamp off after delay
                 self.delay(name='lamp_off', event_type=None, delay=self.target_timer-0.5, handler=self.lamp_off)
                 if self.index == 2:
                      self.game.sound.play('kick_hurryup')
             else:
                 # cancel repeated call
                 self.cancel_delayed('lit_jackpot')
                 # reset
                 self.delay(name='reset_kicks', event_type=None, delay=2, handler=self.reset_kicks)
                 self.layer = self.score_layer.set_text('KICK AGAIN...',2,4)

        def kicks_hit(self):
             self.game.sound.play('kick')
             self.game.score(self.kicks_score)
             # decrease kicks
             self.kicks_setting -= 1
             self.kicks_layer.set_text(str(self.kicks_setting))
             self.play_animation()
             if self.kicks_setting == 0: # Jackpot ready
                 self.game.effects.gi_off()
                 self.lite_jackpot = True
                 self.game.effects.raise_droptarget()
                 self.game.sound.play('jackpot_lit')
                 # start jackpot sequence
                 self.lit_jackpot()

        def bumper(self):
             self.game.score(10)
             self.game.sound.play('bumper')
             # raise kick_value
             self.raise_kicks()

        def raise_kicks(self):
             self.kicks_score += 10000
             self.value_layer.set_text(locale.format("%d", self.kicks_score, True))

        def target_hit(self,id):
             if self.lite_jackpot == True:
                 # check if hit-target == jackpot-target
                 if self.roadkingslamps[id] == self.temp_list[self.index]: # Jackpot!
                     self.cancel_delayed('lit_jackpot')
                     #play sounds
                     self.game.sound.play('jackpot')
                     # lampshow
                     self.game.lampctrl.play_show('mode_jackpot', False, 'None')
                     # jackpot_animation() TO DO
                     self.layer = self.score_layer.set_text(locale.format("%d", self.jackpot_value, True), seconds=2, blink_frames=2)
                     # score jackpot
                     self.game.score(self.jackpot_value)
                     # reset
                     self.delay(name='reset_kicks', event_type=None, delay=2, handler=self.reset_kicks)
                 else:
                     self.game.effects.drive_lamp_schedule(self.roadkingslamps[id], schedule=0x99999999, cycle_seconds=1, now=True)
                     self.game.sound.play('jackpot_missed')

        def stop_kickstartking(self):
             self.callback('kickstartking')
             self.game.coils.outhole.pulse(30)

## switches

        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_1s(self,sw):
             self.game.effects.eject_ball(location='upperLkicker')
             self.update_lamps()
             return True

        def sw_outhole_active(self,sw):
             self.delay(name='stop_kickstartking', event_type=None, delay=1.0, handler=self.stop_kickstartking)
             self.cancel_delayed('lit_jackpot')
             self.clear_lamps()
             return True

        def sw_Lspinner_active(self, sw):
             return True

        def sw_Leject_active(self,sw):
             return True

        def sw_Leject_active_for_2s(self,sw):
             self.game.effects.eject_ball('Ceject')

        def sw_Ceject_active(self,sw):
             return True

        def sw_Ceject_active_for_2s(self,sw):
             self.game.effects.eject_ball('Ceject')

        def sw_slingL_active(self,sw):
             self.game.lampctrl.play_show('sling_left', False, 'None')
             self.kicks_hit()
             return True

        def sw_slingR_active(self,sw):
             self.game.lampctrl.play_show('sling_right', False, 'None')
             self.kicks_hit()
             return True

        def sw_bumperL_active(self,sw):
             self.bumper()
             return True

        def sw_bumperU_active(self,sw):
             self.bumper()
             return True

        def sw_bumperR_active(self,sw):
             self.bumper()
             return True

        def sw_bumperD_active(self,sw):
             self.bumper()
             return True

        def sw_dropTarget_active_for_500ms(self,sw):
              self.game.effects.raise_droptarget()
              return True

        def sw_targetR_active(self,sw):
             self.target_hit(0)
             return True

        def sw_targetO_active(self,sw):
             self.target_hit(1)
             return True

        def sw_targetA_active(self,sw):
             self.target_hit(2)
             return True

        def sw_targetD_active(self,sw):
             self.target_hit(3)
             return True

        def sw_targetK_active(self,sw):
             self.target_hit(4)
             return True

        def sw_targetI_active(self,sw):
             self.target_hit(5)
             return True

        def sw_targetN_active(self,sw):
             self.target_hit(6)
             return True

        def sw_targetG_active(self,sw):
             self.target_hit(7)
             return True

        def sw_targetS_active(self,sw):
             self.target_hit(8)
             return True
