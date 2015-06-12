# Control for missions and main modes

__author__="Pieter"
__date__ ="$Okt 25, 2012 20:30:27 PM$"

import procgame
import locale
import random
from procgame import *

from easy_rider import *
from multibastard import *
from kickstart_king import *
#from race_champion import *

#all necessary paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"

class MissionsModes(game.Mode):

        def __init__(self, game, priority):
            super(MissionsModes, self).__init__(game, priority)
            self.name_layer = dmd.TextLayer(128/2, 7, self.game.fonts['num_09Bx7'], "center")
            self.info_layer = dmd.TextLayer(128/2, 18, self.game.fonts['07x5'], "center")

            #setup sound
            self.game.sound.register_sound('rkmode_started', sound_path+'rkmode_started1.ogg')
            self.game.sound.register_sound('startyourengine', speech_path+"startyourengine.wav")
            self.game.sound.register_sound('letsgoforride', speech_path+"letsgoforride.ogg")

            self.name_text =''
            self.info_text =''

            self.mission_lamps = ['bonus1k','bonus2k','bonus3k','bonus4k','bonus5k','bonus6k','bonus7k','bonus8k','bonus9k', 'bonus10k']
            self.mission_list = [0,0,0,0,0,0,0,0,0,0]

            self.modes_lamps = ['raceChampion','kickstartKing','bumperBastard','easyRider']
            self.rkmodes_list = [0,0,0,0]
            self.current_mode_num = 0
            self.choice_id =0

            self.mode_enabled = False

            #setup game modes
            #self.race_champion = Racechampion(self.game, 81)
            #self.race_champion.callback = self.mode_callback
            self.kickstart_king = Kickstartking(self.game, 82)
            self.kickstart_king.callback = self.mode_callback
            self.multibastard = Multibastard(self.game, 83)
            self.multibastard.callback = self.mode_callback
            self.easyrider = Easyrider(self.game, 84)
            self.easyrider.callback = self.mode_callback

            self.reset()

        def reset(self):
            self.reset_lamps()

        def mode_started(self):
            print("Debug, Mission Control Started")
            #load player stats
            self.current_mode_num = self.game.get_player_stats('current_mode_num')
            self.rkmodes_list = self.game.get_player_stats('mode_status_tracking')
            self.mode_enabled = self.game.get_player_stats('mode_enabled')
            self.mission_list = self.game.get_player_stats('mission_status_tracking')

            #setup rkmode list
            self.unplayed_rkmodes()

        def mode_stopped(self):
            print("Debug, Mission Control Stopped")
            #update player stats
            self.game.set_player_stats('current_mode_num',self.current_mode_num)
            self.game.set_player_stats('mode_status_tracking',self.rkmodes_list)
            self.game.modes.remove(self.multibastard)
            self.game.modes.remove(self.easyrider)

        def mode_tick(self):
            pass

## lamps & animations

        def reset_lamps(self):
            #loop round and turn off all lamps
            for i in range(len(self.modes_lamps)):
                self.game.effects.drive_lamp(self.modes_lamps[i],'off')

            self.mode_start_lamp(self.mode_enabled)

        def update_lamps(self):
            #current mode
            self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'slow')

            #completed modes
            for i in range(len(self.modes_lamps)):
                if self.rkmodes_list[i]==1:
                    self.game.effects.drive_lamp(self.modes_lamps[i],'on')

            #mode start
            #self.update_ramp_lamps()
            self.mode_start_lamp(self.mode_enabled)

            #update mission lamps on bonus 1k...10k
            self.update_mission_lamps()

        def mode_start_lamp(self,flag):
            if flag and self.game.get_player_stats('ramp_state') == False:
                self.game.effects.drive_lamp('megaScore','medium')
            else:
                self.game.effects.drive_lamp('megaScore','off')

        def update_ramp_lamps(self):
            # to update lamp after ramp move (called from effects)
            self.mode_start_lamp(self.mode_enabled)

        def clear_layer(self):
            self.layer=None

# Mission control

        def update_missions(self,mission_id):
             self.mission_list = self.game.get_player_stats('mission_status_tracking')
             # mission_id -1 to correspond with list
             self.mission_list[mission_id-1] = 1
             self.game.set_player_stats('mission_status_tracking',self.mission_list)
             print("Mission list: ", self.mission_list)
             self.update_mission_lamps()
             self.check_missions()

        def check_missions(self):
             count_missions = self.count_missions()
             count_modes = self.count_modes()
             if count_missions >= 1 and count_modes == 0:
                 print("En nu kan de eerste mode gestart worden!")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 3 and count_modes == 1:
                 print("En nu kan de tweede mode gestart worden!")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 5 and count_modes == 2:
                 print("En nu kan de derde mode gestart worden!")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 7 and count_modes == 3:
                 print("En nu kan de vierde mode gestart worden!")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 10 and count_modes == 4:
                 print("En nu kan het eindspel gestart worden!")
                 self.game.set_player_stats('mode_enabled',True)
                 #self.activate_rkmode(True)

        def update_mission_lamps(self):
             for i in range(len(self.mission_lamps)):
                if self.mission_list[i]:
                    self.game.effects.drive_lamp(self.mission_lamps[i],'on')

        def count_missions(self):
             count_rkmissions = 0
             for i in range(len(self.mission_list)):
                if self.mission_list[i]:
                    count_rkmissions +=1
             print("Missions nr: ", count_rkmissions)
             return count_rkmissions

## mode functions

        def mode_callback(self,mode_name):
             print("In mode callback")
             if mode_name == 'multibastard':
                  self.game.modes.remove(self.multibastard)
             if mode_name == 'easyrider':
                  self.game.modes.remove(self.easyrider)
             if mode_name == 'kickstartking':
                  self.game.modes.remove(self.kickstart_king)
             #if mode_name == 'racechampion':
             #     self.game.modes.remove(self.racechampion)
             # restart main theme music and update lamps and gi
             self.game.effects.rk_play_music()
             self.game.effects.gi_on()
             self.game.update_lamps()

        def activate_rkmode(self, flag=False):
             self.mode_enabled = flag
             self.mode_start_lamp(flag)

        def count_modes(self):
             count_rkmodes = 0
             for i in range(len(self.rkmodes_list)):
                if self.rkmodes_list[i]:
                    count_rkmodes +=1
             print("Modes nr: ", count_rkmodes)
             return count_rkmodes

        def unplayed_rkmodes(self,dirn=None):

            #turn off current mode lamp
            self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'off')

            #create list of unplayed rkmode numbers
            choice_list=[]
            for i in range(len(self.rkmodes_list)):
                if self.rkmodes_list[i]==0:
                    choice_list.append(i)

            #adjust choice number
            if dirn=='left':
                self.choice_id -=1
            elif dirn=='right':
                self.choice_id +=1
            else:
                self.choice_id = random.randint(0, len(choice_list)-1)

            #create wrap around
            if self.choice_id>len(choice_list)-1:
                self.choice_id=0
            elif self.choice_id<0:
                self.choice_id=len(choice_list)-1

            #set new mode number
            self.current_mode_num = choice_list[self.choice_id]

            #update lamps
            self.update_lamps()

            #print("mode now active:"+str(self.modes_lamps[self.current_mode_num]))


        def move_left(self):
            self.unplayed_rkmodes('left')
            #self.game.coils.rearFlash_upLeftkicker.schedule(schedule=0x30003000 , cycle_seconds=1, now=True)

        def move_right(self):
            self.unplayed_rkmodes('right')
            #self.game.coils.rearFlash_upLeftkicker.schedule(schedule=0x30003000 , cycle_seconds=1, now=True)

        def eject_ball(self):
            self.game.effects.eject_ball(location='upperLkicker')

        def start_rkmode(self):
            if self.mode_enabled:
                #play sound
                #self.game.sound.fadeout_music()
                #self.game.sound.play("rkmode_started")

                if self.current_mode_num==0:
                    self.name_text = 'RACE CHAMPION'
                    self.info_text = 'SHOOT MOVING SHOT'
                    #self.game.sound.play('')

                elif self.current_mode_num==1:
                    self.name_text = 'KICKSTART KING'
                    self.info_text = 'COLLECT KICKS FOR JACKPOT'
                    #self.game.sound.play('')

                elif self.current_mode_num==2:
                    self.name_text = 'MULTI BASTARD'
                    self.info_text = 'PLAY MULTIBALL'
                    self.game.sound.play('startyourengine')

                elif self.current_mode_num==3:
                    self.name_text = 'EASY RIDER'
                    self.info_text = 'SHOOT ALL LIT SHOTS'
                    self.game.sound.play('letsgoforride')


                anim = dmd.Animation().load(dmd_path+"start_rkmode.dmd")
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames,hold=True,frame_time=2)

                self.animation_layer.add_frame_listener(-1,self.mode_text)

                self.ssd_count=0#temp fix for frame_listener multi call with held
                self.animation_layer.add_frame_listener(-1,self.rkmode_start_delay)


                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.name_layer,self.info_layer])

                self.mode_enabled=False
                self.game.set_player_stats('mode_enabled',False)

            else:
                self.delay(name='eject_delay', event_type=None, delay=0.5, handler=self.eject_ball)


        def mode_text(self):
            self.name_layer.set_text(self.name_text)
            self.info_layer.set_text(self.info_text)


        def rkmode_start_delay(self):
            time = 5

            if self.ssd_count==0: #make sure the following delays only get called once
                #self.delay(name='rkmode_timeout', event_type=None, delay=self.timer, handler=self.end_rkmode)
                self.delay(name='rkmode_delay', event_type=None, delay=time, handler=self.add_selected_rkmode)
                #self.delay(name='eject_delay', event_type=None, delay=time+5, handler=self.eject_ball)
                self.delay(name='clear_delay', event_type=None, delay=time+1, handler=self.clear_layer)
                self.ssd_count+=1
                #update mode completed status tracking
                self.rkmodes_list[self.current_mode_num] =1
                self.update_lamps()

        def add_selected_rkmode(self):

            print("Adding rkmode Mode: "+str(self.current_mode_num))
            if self.current_mode_num==0:
                #self.game.modes.add(self.race_champion)
                self.delay(name='eject_delay', event_type=None, delay=3, handler=self.eject_ball)
            elif self.current_mode_num==1:
                  self.game.modes.add(self.kickstart_king)
                  #self.delay(name='eject_delay', event_type=None, delay=3, handler=self.eject_ball)
            elif self.current_mode_num==2:
                  self.game.modes.add(self.multibastard)
            elif self.current_mode_num==3:
                  self.game.modes.add(self.easyrider)
                  #self.delay(name='eject_delay', event_type=None, delay=3, handler=self.eject_ball)


        def end_rkmode(self):

            #remove the active rkmode
            self.remove_selected_rkmode()

            #display mode total on screen
            #bgnd_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+"end_rkmode.dmd").frames[0])
            #self.info_layer.set_text(locale.format("%d",self.game.get_player_stats('last_mode_score'),True))
            #self.layer = dmd.GroupedLayer(128, 32, [bgnd_layer,self.name_layer,self.info_layer])

            #update mode completed status tracking
            self.rkmodes_list[self.current_mode_num] =1

            #clean up
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)
            self.update_lamps()


        def remove_selected_rkmode(self):
            print("Removing rkmode Mode: "+str(self.current_mode_num))
            if self.current_mode_num==0:
                #self.game.modes.remove(self.race_champion)
                self.game.modes.remove(self.multibastard)
            elif self.current_mode_num==1:
                #self.game.modes.remove(self.kickstart_king)
                self.game.modes.remove(self.multibastard)
            elif self.current_mode_num==2:
                self.game.modes.remove(self.multibastard)
            elif self.current_mode_num==3:
                #self.game.modes.remove(self.easy_rider)
                self.game.modes.remove(self.easyrider)

## switches

        def sw_upperLkicker_active_for_500ms(self,sw):
             #if self.mode_enabled:
             if self.mode_enabled and self.game.get_player_stats('multiball_running')==False:
                 self.start_rkmode()

        def sw_RrampExit_active(self, sw):
             if self.mode_enabled and self.game.get_player_stats('multiball_running')==False:
                 #play sound
                 self.game.effects.rk_play_music('stop')
                 self.game.sound.play("rkmode_started")

        def sw_upperLkicker_active(self,sw):
             if self.mode_enabled and self.game.get_player_stats('multiball_running')==False:
                 return procgame.game.SwitchStop

        def sw_slingL_active(self,sw):
             self.move_right()

        def sw_slingR_active(self,sw):
             self.move_left()
