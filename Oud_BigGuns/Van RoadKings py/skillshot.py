# skillshot

__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
import locale
from procgame import *
from random import *
import random

#all necessary paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"

#Steven: nog te doen: lanechange uit gedurende skillshot, evenals de bijbehorende lampjes

class Skillshot(game.Mode):

        def __init__(self, game, priority):
            super(Skillshot, self).__init__(game, priority)

            self.text_layer = dmd.TextLayer(90, 12, self.game.fonts['num_09Bx7'], "center", opaque=False)

            self.game.sound.register_sound('skillshot_made', speech_path+"great_shot.wav")
            self.game.sound.register_sound('skillshot_made', speech_path+'skillshot.wav')

            self.lamps = ['Ctimelock','Clock']
            self.lanelamps = ['lane1','lane2']
            self.choice = 0
            #Steven:
            self.skillshot_made = False
            #self.skill_timer =7 #VIA MENU
            self.skill_timer = self.game.user_settings['Gameplay (Feature)']['Skillshot Timer']
            self.skill_value_start = 250000 #VIA MENU
            #self.skill_value_start = self.game.user_settings['Gameplay (Feature)']['Skillshot Start']
            self.skill_value_boost = 250000 #VIA MENU
            #self.skill_value_boost = self.game.user_settings['Gameplay (Feature)']['Skillshot Boost']
            self.count = 0
            self.skill_value = 0

            self.reset()

        def reset(self):
           pass

        def mode_started(self):
            print("Debug, Skilshot Mode Started")
            #self.activate_lamps()
            #load player specific data
            self.count = self.game.get_player_stats('skillshots')
            # calculate value
            self.skill_value = self.skill_value_boost*self.count +self.skill_value_start
            self.start_skill()

        def mode_stopped(self):
            print("Debug, Skillshot Mode Ended")
            #save player specific data
            self.game.set_player_stats('skillshots',self.count)
            self.game.update_lamps()

        def mode_tick(self):
            pass

## lamps & animation

        def activate_lamps(self):
             for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'superfast')
                #self.game.sound.play("Superskill")

        def clear_lamps(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'off')

        def clear_all_lamps(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'off')
            self.game.effects.drive_lamp(self.lanelamps[self.choice],'off')

        def restore_lamps(self):
            self.game.lampctrl.restore_state('game')

        def update_lamps(self):
            #self.game.effects.drive_lamp(self.lanelamps[self.choice],'medium')
            pass

        def play_animation(self):
             #set layers for animation
             anim = dmd.Animation().load(dmd_path+'skillshot.dmd')
             self.bgnd_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=7)
             self.text_layer.set_text(locale.format("%d",self.skill_value,True),blink_frames=2)
             self.layer = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.text_layer])

## mode functions

        def start_timer(self):
             # start timer
             self.delay(name='grace_time', event_type=None, delay=self.skill_timer, handler=self.grace_time)

        def start_skill(self):
             #generate random lamp from list
             #self.choice = random.randrange(0, len(self.lanelamps),1)
             self.choice = random.randint(0, len(self.lanelamps)-1)
             print("lamp_keuze: "+self.lanelamps[self.choice])
             self.game.effects.drive_lamp(self.lanelamps[self.choice],'medium')
             #self.update_lamps()

        def lanes(self,id):
                #Steven: skillshotmade toegevoegd om niet 2 of 3 keer skillshotwaarde te krijgen
             if id == self.choice and self.skillshot_made == False :
                  # skillshot scored
                  self.game.sound.play('skillshot_made')
                  self.play_animation()
                  self.game.score(self.skill_value)
                  # raise counter
                  self.count+=1
                  # update missions
                  self.game.base_game_mode.missions_modes.update_missions(1)
                  # clear mode after delay
                  self.delay(name='clear', event_type=None, delay=2, handler=self.clear)
                  self.skillshot_made = True 
             else:
                  #self.game.sound.play('skillshot_missed')
                  self.clear()

        def start_superskill(self):
             self.game.coils.Lgate.pulse(0)

        def super_skill(self):

            # cancel delays
            self.cancel_delayed('grace_time')
            self.cancel_delayed('clear')
               
            self.game.sound.play('skillshot_made')

            self.play_animation()

            # clear mode after delay (call drain save first)
            self.delay(name='clear', event_type=None, delay=2, handler=self.drain_save)

            # raise counter
            self.count+=1

            # add score
            self.game.score(self.skill_value)

            # update missions
            self.game.base_game_mode.missions_modes.update_missions(1)

            #lamp show - and restore previous lamps
            #self.game.lampctrl.save_state('game')
            #self.game.lampctrl.play_show('success', repeat=False, callback=self.restore_lamps)

        def drain_save(self):
             # add time to ballsaver in case of SDTM from Ceject
             self.game.ball_save.add(add_time=2, allow_multiple_saves=False)
             self.clear()

        def grace_time(self):
             self.clear_lamps()
             self.delay(name='clear', event_type=None, delay=1.5, handler=self.clear)

        def clear(self):
             self.layer = None
             self.game.coils.Lgate.disable()
             self.game.effects.eject_ball(location='Ceject')
             self.clear_all_lamps()
             self.game.modes.remove(self)

## switches

        def sw_lane1_active(self, sw):
             self.lanes(0)
             return procgame.game.SwitchStop

        def sw_lane2_active(self, sw):
             self.lanes(1)
             return procgame.game.SwitchStop

        def sw_Ceject_active(self,sw):
             return procgame.game.SwitchStop

        def sw_Ceject_active_for_250ms(self,sw):
             self.super_skill()

        def sw_CrampEnter_active(self,sw):
             self.clear()

        def sw_shooterLane_open_for_25ms(self,sw):
             if self.game.ball_starting:
                  # start timer
                  self.start_timer()
                  # start superskillshot
                  if self.game.switches.flipperLwL.is_active():
                       self.start_superskill()

        # end mode when a ball drains
        def sw_outhole_active(self,sw):
             self.clear()

