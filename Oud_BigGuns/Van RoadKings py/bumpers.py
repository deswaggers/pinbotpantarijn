#
# Bumpers
#
# Game mode that uses bumperhits to achieve different levels
# Each level has its own award
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"

import procgame
from procgame import *
from quick_multiball import *
from tunnel_trial import *

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"

class Bumpers(game.Mode):

        def __init__(self, game, priority):
            super(Bumpers, self).__init__(game, priority)

            self.quick_multiball = Quickmb(self.game, priority+40) # reference to quick multiball
            self.tunnel_trial = Tunneltrial(self.game, priority+40) # reference to tunnel trial

            self.title_layer = dmd.TextLayer(100, 4, self.game.fonts['num_09Bx7'], "center", opaque=False)
            self.value_layer = dmd.TextLayer(100, 14, self.game.fonts['num_14x10'], "center", opaque=False)
            self.level_layer = dmd.TextLayer(100, 27, self.game.fonts['tiny7'], "center", opaque=False)

            self.game.sound.register_sound('bumper', sound_path+"bumpers.aiff")
            self.game.sound.register_sound('bumper', sound_path+"bumpers1.aiff")
            self.game.sound.register_sound('bigbumpers', speech_path+"big_men.aiff")
            self.game.sound.register_sound('bigbumpers', speech_path+"bumpers_women1.aiff")
            self.game.sound.register_sound('bigbumpers', sound_path+"super_jets.aiff")
            self.game.sound.register_sound('bigbumpers', speech_path+"big_men1.aiff")
            self.game.sound.register_sound('bigbumpers', speech_path+"bumpers_women2.aiff")

            #self.bumpers_default = 10 #VIA MENU
            self.bumpers_default = self.game.user_settings['Gameplay (Feature)']['Bumpers Default']
            #self.bumpers_raise = 5 #VIA MENU
            self.bumpers_raise = self.game.user_settings['Gameplay (Feature)']['Bumpers Raise']

            self.start_miles = False
            self.miles_count = 0
            self.start_bigbumpers = False
            self.miles_score = 110
            self.bumper_score = 1010
            self.big_bumper_score = 100000

            self.animation_status='ready'

        def mode_started(self):
            print("Debug, Bumpers Mode Started")
            #get player specific data
            self.level = self.game.get_player_stats('bumper_level')
            self.calculate_count()
            # Start level for 1st level
            if self.level == 1:
                 self.start_level_mode()

        def mode_stopped(self):
            print("Debug, Bumpers Mode Ended")
            #save player specific data
            self.game.set_player_stats('bumper_level',self.level)

## Sounds & Animations

        def play_sound(self):
            if self.start_bigbumpers:
                self.game.sound.play('bigbumpers')
            else:
                self.game.sound.play('bumper')

        def play_animation(self,opaque=False, repeat=False, hold=False, frame_time=8):

            if self.animation_status=='ready':

               if self.start_bigbumpers:
                   anim = dmd.Animation().load(dmd_path+'big_bumpers.dmd')
               else:
                   anim = dmd.Animation().load(dmd_path+'bumpers.dmd')

               self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=opaque, repeat=repeat, hold=hold, frame_time=frame_time)
               self.animation_layer.add_frame_listener(-1, self.animation_ended)
               self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.value_layer, self.level_layer])
               self.animation_status = 'running'

        def animation_ended(self):
            self.animation_status = 'ready'
            self.layer = None

## mode functions

        def calculate_count(self):
            self.bumpers_count =  self.bumpers_default + (self.bumpers_raise*self.level)

        def update_count(self):
            if self.bumpers_count >0:

                if self.start_miles:
                    self.miles_count +=1
                    self.game.add_player_stats('miles_collected',1)
                    #self.title_layer.set_text('MILES')
                    self.value_layer.set_text(str(self.miles_count))

                else:
                    #self.title_layer.set_text('BUMPERS')
                    self.value_layer.set_text(str(self.bumpers_count))

                self.bumpers_count -=1
                self.level_layer.set_text('level '+str(self.level))

            elif self.bumpers_count ==0:
                  # raise level
                  self.level += 1
                  # calculate count
                  self.calculate_count()
                  # start level mode
                  self.start_level_mode()

        def start_level_mode(self):

             print("next bumper level: ", self.level)
             print("bumpers count: ", self.bumpers_count)

             # check level
             if self.level == 1 or self.level == 6: # Basic level
                   # Reset Big Bumpers and Miles
                   self.start_bigbumpers = False
                   self.start_miles = False
                   self.title_layer.set_text('BUMPERS')

             elif self.level == 2 or self.level == 7: # Quick Multiball
                   # start quick multiball
                   self.start_quickmball()

             elif self.level == 3 or self.level == 8: # Big Bumpers
                   #start Big Bumpers
                   self.start_bigbumpers = True
                   # update missions for achieving bumper level 3
                   self.game.base_game_mode.missions_modes.update_missions(9)

             elif self.level == 4 or self.level == 9: # Miles
                   #end Big Bumpers
                   self.start_bigbumpers = False
                   #start Miles
                   self.start_miles = True
                   self.title_layer.set_text('MILES')

             elif self.level == 5 or self.level == 10: # Tunnel Trial
                   # end Miles
                   self.start_miles = False
                   self.title_layer.set_text('BUMPERS')
                   # start Tunnel Trial
                   self.start_tunneltrial()

             else: # Reset level and count
                   self.level = 1
                   self.calculate_count()

        def start_quickmball(self):
             self.game.modes.add(self.quick_multiball)

        def start_tunneltrial(self):
             self.game.modes.add(self.tunnel_trial)

        def bumpers_score(self):
            if self.start_miles:
                self.game.score(self.miles_score)
            elif self.start_bigbumpers:
                  self.game.score(self.big_bumper_score)
            else:
                self.game.score(self.bumper_score)

## switches

        def sw_bumperU_active(self, sw):
            self.play_sound()
            self.update_count()
            self.bumpers_score()
            self.play_animation()

        def sw_bumperL_active(self, sw):
            self.play_sound()
            self.update_count()
            self.bumpers_score()
            self.play_animation()

        def sw_bumperR_active(self, sw):
            self.play_sound()
            self.update_count()
            self.bumpers_score()
            self.play_animation()

        def sw_bumperD_active(self, sw):
            self.play_sound()
            self.update_count()
            self.bumpers_score()
            self.play_animation()

