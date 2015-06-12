#
# Combo's
#
# Game mode for scoring following combo's:
# - centerramp + leftloop
# - centerramp + rightloop (ramp up!)
# - centerramp + rightramp
#

__author__="Pieter"
__date__ ="$13 Nov 2012 20:36:37 PM$"


import procgame
import locale
import logging
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Combo(game.Mode):

        def __init__(self, game, priority):
            super(Combo, self).__init__(game, priority)

            #register sound effects files
            #self.game.sound.register_sound('combo_made', sound_path+"combo_made.ogg")
            self.game.sound.register_sound('combo_made', sound_path+"outlanes.aiff")
            self.game.sound.register_sound('combos_complete', sound_path+"outlanes.aiff")

            #register animation layers
            self.combo_text = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center", opaque=False)
            self.info_text = dmd.TextLayer(128/2, 20, self.game.fonts['num_09Bx7'], "center", opaque=False).set_text("COMBO") #num_09Bx7 num_14x10
            #self.info_text = dmd.TextLayer(128/2, 17, self.game.fonts['num_14x10'], "center", opaque=False).set_text("12345") #num_09Bx7 num_14x10

            #register lampshow
            self.game.lampctrl.register_show('combo_show', lampshow_path+"succes.lampshow")

            #self.combo_flag = [False,False,False]
            self.combo_flag = [0,0,0]
            self.spinner = True
            self.runder = True


            self.combo_value = 500000 #VIA MENU
            #self.combo_value = self.game.user_settings['Gameplay (Feature)']['Combo Value']

        def mode_started(self):
             print("Debug, Combo Mode Started")
             self.combo_flag = self.game.get_player_stats('combo_flag')
             #print(self.combo_flag)

        def mode_stopped(self):
             print("Debug, Combo Mode Ended")


## lamps and animations

        def update_lamps(self):
             pass

        def play_animation(self):
             anim = dmd.Animation().load(dmd_path+'arrows_ttt.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=3)
             #self.animation_layer.add_frame_listener(-1, self.clear_layer)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.combo_text, self.info_text])
             self.delay(name='clear_display', event_type=None, delay=3.5, handler=self.clear_layer)

        def clear_layer(self):
             self.layer = None

## mode functions

        def check_combos(self):
             count = 0
             for i in range(len(self.combo_flag)):
                  if self.combo_flag[i]: # check if all 3 are made
                      count += 1
                  if self.combo_flag[i] == 3: #check if any 3 are made
                      count = 3
             if count >=3:
                 # combos complete
                 self.game.sound.play('combos_complete')
                 self.combo_text.set_text("COMPLETED!",3,3)#on for 3 seconds 3 blinks
                 # update missions for achieving Combo's
                 self.game.base_game_mode.missions_modes.update_missions(5)
             return count

        def set_combo(self, id=0):
             #play sound, lightshow and animation
             self.game.sound.play('combo_made')
             self.game.lampctrl.play_show('combo_show', False, 'None')
             self.play_animation()
             #score combo value
             self.game.score(self.combo_value)
             #set flag
             #self.combo_flag[id] = True
             self.combo_flag[id] += 1
             self.game.set_player_stats('combo_flag',self.combo_flag)
             #check for combos completed
             self.check_combos()

        def close_gate(self):
             self.game.coils.Lgate.disable()

        def set_spinner(self):
             self.spinner = True

        def set_Runder(self):
             self.runder = True

## Switches Combo's

        def sw_lane3_active(self,sw):
             if self.game.switches.CrampEnter.time_since_change() < 4:
                # update lamps right ramp
                    self.game.lamps.Rtimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=3, now=True)
                    self.game.lamps.Rlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=3, now=True)
                    self.game.lamps.Rextraball.schedule(schedule=0x0f0f0f0f, cycle_seconds=3, now=True)

        def sw_CrampRexit_active(self, sw):
                self.game.effects.drive_lamp('bonusholdWL','timeout',time=3)

        def sw_Lspinner_active(self, sw):
             if self.spinner:
                 if self.game.switches.CrampRexit.time_since_change() < 3:
                     self.spinner = False
                     self.combo_text.set_text("TURN LEFT",3,4)#on for 3 seconds 4 blinks
                     self.set_combo(id=0)
                     self.delay(name='set_spinner', event_type=None, delay=3, handler=self.set_spinner)

        def sw_RrampExit_active(self,sw):
             if self.game.switches.CrampEnter.time_since_change() < 5 and self.game.switches.lane3.time_since_change() < 3:
                 self.combo_text.set_text("JUMP",3,4)#on for 3 seconds 4 blinks
                 self.set_combo(id=1)

        def sw_Rrollunder_active(self,sw):
             if self.runder:
                 if self.game.switches.CrampEnter.time_since_change() < 4 and self.game.switches.lane3.time_since_change() < 2:
                     self.runder = False
                     self.combo_text.set_text("TURN RIGHT",3,4)#on for 3 seconds 4 blinks
                     self.set_combo(id=2)
                     # open left gate
                     self.game.coils.Lgate.enable()
                     self.delay(name='close_gate', event_type=None, delay=2, handler=self.close_gate)
                     self.delay(name='set_runder', event_type=None, delay=3, handler=self.set_Runder)

