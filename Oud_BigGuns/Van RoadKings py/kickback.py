#
# kickback
#
# Game mode that controls the kickback
# 
__author__="Steven"
__date__ ="$Sep 11, 2012 16:36:37 PM$"


import procgame
import locale
from procgame import *
import random

game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"


class Kickback(game.Mode):

        def __init__(self, game, priority):
            super(Kickback, self).__init__(game, priority)

            self.title_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_09Bx7'], "center", opaque=True)

            self.game.sound.register_sound('powerkick', sound_path+"bumpers.aiff")
            self.game.sound.register_sound('superkick', sound_path+"super_jets.aiff")

            self.kickback_state = 'normal'
            self.kickback_ready = True
            self.grace_time = 3

        def reset(self):
            pass

        def mode_started(self):
            print("Debug, Kickback Mode Started")
            self.update_kickback()

        def mode_stopped(self):
            # substract superkickback if ball is lost
            if self.kickback_state=='super':
                self.game.set_player_stats('kickback','normal')
            self.clear_lamps()
            print("Debug, Kickback Mode Ended")

## lamps

        def update_lamps(self):
            if self.kickback_state=='normal' or self.kickback_state=='super':
                    self.game.effects.drive_lamp('kickback','smarton')
            else:
                    self.game.effects.drive_lamp('kickback','off')

        def clear_lamps(self):
             self.game.effects.drive_lamp('kickback','off')

## Sound & Animations

        def play_sound(self):
            if self.kickback_state=='super':
                self.game.sound.play('superkick')
            else:
                self.game.sound.play('powerkick')

        def play_animation(self,opaque=False, repeat=False, hold=False, frame_time=10):
            #anim = dmd.Animation().load(dmd_path+'kickback.dmd')
            #self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=opaque, repeat=repeat, hold=hold, frame_time=frame_time)
            #self.animation_layer.add_frame_listener(-1, self.clear_layer)
            #self.layer = dmd.GroupedLayer(128, 32, [self.title_layer])

            self.layer = self.title_layer
            self.delay(name='clear_layer', event_type=None, delay=1.5, handler=self.clear_layer)

        def clear_layer(self):
            self.layer = None

## mode functions

        def update_kickback(self):
             self.kickback_state = self.game.get_player_stats('kickback')
             self.update_lamps()

        def raise_kickback(self): # called from other modes to raise kickback
             self.kickback_state = self.game.get_player_stats('kickback')
             if self.kickback_state == False:
                 self.kickback_state = 'normal'
             elif self.kickback_state == 'normal':
                   self.kickback_state = 'super'
             else:
                   self.kickback_state = 'super'
             self.game.set_player_stats('kickback',self.kickback_state)
             self.update_lamps()

        def lower_kickback(self):
             if self.kickback_state == 'super':
                 self.kickback_state = 'normal'
             elif self.kickback_state == 'normal':
                   self.kickback_state = False
             print(self.kickback_state)
             self.game.set_player_stats('kickback',self.kickback_state)
             self.update_lamps()

        def kick_back(self):

            # superkickback
            if self.kickback_state == 'super':
                self.game.coils.kickback.pulse(60)
                self.game.score(100000)
                # play animation
                self.title_layer.set_text('SUPERKICK')
                self.play_animation()

            # regular kickback
            elif self.kickback_state == 'normal':
                  self.game.coils.kickback.pulse(30)
                  self.game.score(1000)
                  # play animation
                  self.title_layer.set_text('POWERKICK')
                  self.play_animation()

            else:
                 self.game.score(100)

        def kickback_reset(self):
             self.kickback_ready = True

        def grace_period(self):
             self.game.effects.drive_lamp('kickback','medium')
             self.delay(name='lower_kickback', event_type=None, delay=self.grace_time, handler=self.lower_kickback)

## switches

        def sw_outlaneL_active(self, sw):
             if self.kickback_ready:
                 self.kickback_ready = False
                 self.kick_back()
                 self.play_sound()
                 self.delay(name='kickback_reset', event_type=None, delay=0.2, handler=self.kickback_reset)
                 if self.kickback_state:
                     self.grace_period()
             #Steven, geluid nog te doen
             if self.game.trough.num_balls_in_play==1 and self.kickback_state== False and self.game.ball_save.timer==0:
                 anim = dmd.Animation().load(dmd_path+'crash.dmd')
                 self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=5)
                 #self.animation_layer.add_frame_listener(-1, self.clear_layer)
                 self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
                 self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

# STEVEN, bij gebruik originele ramp
#        def sw_CrampEnter_active(self, sw):
#             self.game.set_player_stats('kickback','normal')
#             self.update_kickback()



