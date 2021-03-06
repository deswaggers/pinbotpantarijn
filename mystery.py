#
# Mystery Pinbot
# Select random mystery award from mysterylist
# In tournament mode awards are in fixed order
#
__author__="Steven, based on Pieters Road Kings Mystery"
__date__ ="$28 Dec 2016 20:36:37 PM$"

import procgame
from procgame import *
from random import *
import random

# all paths
# All paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Mystery(game.Mode):

        def __init__(self, game, priority):
             super(Mystery, self).__init__(game, priority)

             self.text_layer = dmd.TextLayer(85, 18, self.game.fonts['tiny7'], "center", opaque=False) #tiny7, 07x5

             #self.game.lampctrl.register_show('mystery_show', lampshow_path+"mystery.lampshow")


             self.mysterylist =['5000','10.000','Extra Ball','2.500', '7.500']
             self.temp_list =[]

             self.choice = 0
             self.index = len(self.mysterylist)


        def mode_started(self):
             print("Debug, Mystery Mode Started")
             self.lit()

        def mode_stopped(self):
            self.game.update_lamps()
            print("Debug, Mystery Mode Stopped")

## lamps & animations

        def update_lamps(self):
            pass


        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'mystery_inform.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer
             self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

        def mystery_animation(self):
             anim = dmd.Animation().load(dmd_path+'mystery_ani.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=5)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.text_layer])
             # Award at end of animation (after 4s)
             self.delay(name='award_award', event_type=None, delay=4, handler=self.award_award)

        def scroll_list(self):
             # repeat call to itself to scroll to mysterylist
             if self.index > 0:
                 self.index -= 1
                 self.game.sound.play("sound_spark")
                 # set display text
                 self.text_layer.set_text(self.temp_list[self.index])
                 self.delay(name='scroll_list', event_type=None, delay=0.3, handler=self.scroll_list)
             else:
                 self.cancel_delayed('scroll_list')
                 # set display text for final award
                 self.text_layer.set_text(self.mysterylist[self.choice], blink_frames=10)
                 # reset counter index
                 self.index = len(self.mysterylist)

        def clear_layer(self):
            self.layer = None

## mode functions

        def lit(self):
            self.update_lamps()
            self.inform_player()

        def start_feature(self):
             # Mystery feature started from mystery.py

             #stop music, play sound and light
             self.game.sound.fadeout_music(time_ms=100)
             self.game.sound.play("sound_electricity")
             # turn off all lamps and GI
             for lamp in self.game.lamps:
                  lamp.disable()
             self.game.effects.gi_off()
             #play lampshow



             # get award for normal mode
             #last_award = self.game.get_player_stats('mystery_award')
             # Generate random award from listitems
             # If award equals last_award try again, so you won't get the same item twice in a row
             #repeat = True
             self.choice = random.randrange(0, len(self.mysterylist),1)
                 #if self.choice != last_award:
                     #repeat = False
             print("mystery_keuze: "+str(self.choice)+" , "+self.mysterylist[self.choice])

             # make copy of list to shuffle scrolling list in animation
             self.temp_list = list(self.mysterylist)
             shuffle(self.temp_list)

             #play animation with textscrolling
             self.mystery_animation()
             self.scroll_list()

        def award_award(self):
             #award logic
             self.award(self.mysterylist[self.choice])

        def award(self,option):
            self.cancel_delayed('scroll_list')
            self.delay(name='mystery_end', event_type=None, delay=1, handler=self.mystery_end)

            # assignment off the awards,
            if option==self.mysterylist[0]: # 5.000
                print("Mystery award: 5.000")
                self.game.score(5000)
            elif option==self.mysterylist[1]: # 10.000
                print("Mystery award: 10.000")
                self.game.score(10000)
            elif option==self.mysterylist[2]: #Extra Ball
                print("Mystery award: Extra Ball")
                self.game.extra_ball_count()
                self.game.sound.play("speech_2017_extraball2")
                self.game.effects.drive_lamp("shootAgain")
            elif option==self.mysterylist[3]: # 2.500
                print("Mystery award: 2.500")
                self.game.score(2500)
            elif option==self.mysterylist[4]: # 7.500
                print("Mystery award: 7.500")
                self.game.score(7500)

        def mystery_end(self):
             self.clear_layer()
             self.game.effects.gi_on()
             self.game.effects.eject_ball('eject')

             # restart main theme music (not for listnr. 10)
             self.game.sound.play_music('music_galaxy', loops=-1)

             # raise choice nr. and save for next mystery in tournament mode
             #self.game.set_player_stats('mystery_award',self.choice)

             # reset spinner for mystery
             # self.game.base_game_mode.generalplay.spinner_reset()
             # remove mystery mode
             #self.game.base_game_mode.EjectModestart.mode_2.stop_mode2_2sec()
             #self.game..stop_mode2_2sec()

             self.game.modes.remove(self)

## switches

# Mystery feature started from Ceject in general_play.py



