#
# lanes1234 (top rollover & inlanes)
#
# Game mode for 1,2,3,4, lanes
# control for lanechange and bonusmultiplier
# 
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"

import procgame
import locale
import logging
from procgame import *

#all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"


class Lanes1234(game.Mode):

        def __init__(self, game, priority):
            super(Lanes1234, self).__init__(game, priority)

            self.log = logging.getLogger('rk.Lanes1234')

            self.bonus_layer = dmd.TextLayer(96, 4, self.game.fonts['num_09Bx7'], "center", opaque=False)

            self.game.sound.register_sound('lane_on', sound_path+"inlanes_on.aiff")
            self.game.sound.register_sound('lane_off', sound_path+"inlanes_off.aiff")
            self.game.sound.register_sound('lane_complete', sound_path+"inlanes_complete.aiff")

            self.lane_flag = [False,False,False,False]
            self.lamps = ['lane1','lane2','lane3','lane4']

            self.bonusx = 1
            self.hold_bonusx = False

            self.lane_on_value = 1000
            self.lane_off_value = -500
            self.reset()

        def reset(self):
            self.numbers_spotted = 0
            self.lane_flag = [False,False,False,False]
            self.clear_lamps()

        def mode_started(self):
            print("Debug, Lanes1234 Mode Started")
            #load player specific data
            self.lane_flag = self.game.get_player_stats('lanes1234_flag')
            self.numbers_spotted = self.game.get_player_stats('lanes1234_numbers_spotted')
            # if hold_bonusx True, get previous bonus
            if self.game.get_player_stats('hold_bonusx'):
                self.bonusx = self.game.get_player_stats('bonus_x')
            else: # else overwrite previous
                self.game.set_player_stats('bonus_x',self.bonusx)

            #update lamp states
            self.update_lamps()

        def mode_stopped(self):
            #save player specific data
            print("Debug, Lanes1234 Mode Ended")
            self.game.set_player_stats('lanes1234_flag',self.lane_flag)
            self.game.set_player_stats('lanes1234_numbers_spotted',self.numbers_spotted)
            #self.game.set_player_stats('bonus_x',self.bonusx)

        def mode_tick(self):
            pass

## lamps

        def clear_lamps(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'off')

        def completed(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'superfast')

        def update_lamps(self):
            for i in range(len(self.lamps)):
                if self.lane_flag[i]:
                    self.game.effects.drive_lamp(self.lamps[i],'on')

            if self.game.get_player_stats('hold_bonusx'):
                self.game.effects.drive_lamp('holdBonus','on')
            else:
                self.game.effects.drive_lamp('holdBonus','off')

        def clear_layer(self):
            self.layer = None

## mode functions

        def spell_1234(self):
            if self.numbers_spotted ==4:

                #increase bonus x
                #if self.bonusx >=2:
                #    self.bonusx +=2
                #else:
                self.bonusx +=1
                self.game.add_player_stats('bonus_x',1)

                #self.game.set_player_stats('bonus_x',self.bonusx)
                #print("bonus x "+str(self.bonusx))

                anim = dmd.Animation().load(dmd_path+'lanes_ani.dmd')
                self.bgnd_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=5)

                #set text layers
                self.bonus_layer.set_text("BONUS X"+str(self.bonusx),seconds=2)

                #set display layer
                self.layer = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.bonus_layer])
                #set layer clear time
                self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

                if self.bonusx ==11:
                    self.delay(name='bonus_text', event_type=None, delay=2, handler=self.extra_ball_lit)
                elif self.bonusx ==20:
                    self.delay(name='bonus_text', event_type=None, delay=2, handler=self.max_bonus)

                #flash all lamps when completed then reset after delay
                self.completed()
                self.delay(name='reset_lanes', event_type=None, delay=1.5, handler=self.reset)


        def extra_ball_lit(self):
            self.game.extra_ball.lit('Cextraball')


        def max_bonus(self):
            max_bonus_layer = dmd.TextLayer(128/2, 7, self.game.fonts['num_09Bx7'], "center", opaque=False)
            max_bonus_layer.set_text(str(self.bonusx)+"X MAXIMUM BONUS",1.5,10)
            self.layer = max_bonus_layer


        def lanes(self,id):
            if self.lane_flag[id] == False:
                #If lane was off, turn it on
                self.lane_flag[id]=True;
                self.numbers_spotted +=1
                #update player stats var
                self.game.set_player_stats('lanes1234_flag',self.lane_flag)
                #print("lane lamp on: %s "%(self.lamps[id]))
                self.game.score(self.lane_on_value)

                #play sounds
                if self.numbers_spotted ==4:
                    self.game.sound.play('lane_complete')
                else:
                    self.game.sound.play('lane_on')
                    self.game.effects.drive_lamp(self.lamps[id],'on')

            else:
                self.game.score(self.lane_off_value)

                #play sounds
                self.game.sound.play('lane_off')

                #If lane was on, turn it off.
                self.lane_flag[id]=False;
                self.numbers_spotted -=1
                self.game.effects.drive_lamp(self.lamps[id],'off')
                #update player stats var
                self.game.set_player_stats('lanes1234_flag',self.lane_flag)
                #print("lane lamp off: %s "%(self.lamps[id]))

            self.spell_1234()
            #print(self.lane_flag)
            #print(self.numbers_spotted)


        def lane_change(self,direction):
            list = ['lane1','lane2','lane3','lane4']
            flag_orig = self.lane_flag
            flag_new = [False,False,False,False]
            carry = False
            j=0

            if direction=='left':
                start = 0
                end = len(list)
                inc =1
            elif direction=='right':
                start = len(list)-1
                end = -1
                inc =-1

            for i in range(start,end,inc):
                if flag_orig[i]:

                    if direction=='left':
                        j=i-1
                        if j<0:
                            j=3
                            carry = True
                    elif direction=='right':
                        j=i+1
                        if j>3:
                            j=0
                            carry = True

                    flag_new[i] = False
                    flag_new[j]= True

                    self.game.effects.drive_lamp(list[i],'off')
                    self.game.effects.drive_lamp(list[j],'on')

            #update the carry index if required
            if carry and direction=='left':
                flag_new[3]= True
                self.game.effects.drive_lamp(list[3],'on')
            elif carry and direction=='right':
                flag_new[0]= True
                self.game.effects.drive_lamp(list[0],'on')

            self.lane_flag=flag_new
            #print(self.lane_flag)

## switches

        def sw_lane1_active(self, sw):
            self.lanes(0)

        def sw_lane2_active(self, sw):
            self.lanes(1)

        def sw_lane3_active(self, sw):
            self.lanes(2)

        def sw_CrampRexit_active(self, sw):
            self.lanes(2)

        def sw_lane4_active(self, sw):
            self.lanes(3)


        def sw_flipperLwL_active(self, sw):
            self.lane_change('left')

        def sw_flipperLwR_active(self, sw):
            self.lane_change('right')

