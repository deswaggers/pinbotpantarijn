#
# Regular multiball
#
# Main game mode (1 of 4) 
# 2 ball Multiball, lock balls for 3-ball multiball
# Jackpot on rightramp, superjackpot on centerramp
#
__author__="Steven"
__date__ ="$16 Oct 2012 14:24:37 PM$"

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

class Multibastard(game.Mode):
        def __init__(self, game, priority):
            super(Multibastard, self).__init__(game, priority)

            self.log = logging.getLogger('rk.Multibastard')

            self.title_layer = dmd.TextLayer(94, 4, self.game.fonts['07x5'], "center", opaque=False)
            self.timer_layer = dmd.TextLayer(95, 16, self.game.fonts['num_14x10'], "center", opaque=False)
            self.score_layer = dmd.TextLayer(128/2, 14, self.game.fonts['num_14x10'], "center", opaque=False)  #num_09Bx7 num_14x10
            self.value_layer = dmd.TextLayer(128/2, 32-6, self.game.fonts['07x5'], "center", opaque=False)
            #self.value_layer.composite_op = "alpha"

            self.game.sound.register_music('multiball_theme', music_path+"bumperbastard.ogg")
            self.game.sound.register_sound('jackpot', speech_path+"jaackpot.wav")
            self.game.sound.register_sound('jackpotislit', speech_path+"jackpotislit.wav")
            self.game.sound.register_sound('superjackpotislit', speech_path+"superjackpotislit.wav")
            self.game.sound.register_sound('superjackpot', speech_path+"superjackpot.wav")
            self.game.sound.register_sound('ball1locked', speech_path+"mb_ball1captured.wav")
            self.game.sound.register_sound('ball2locked', speech_path+"mb_ball2locked.wav")
            self.game.sound.register_sound('bumper', sound_path+"bumpers1.aiff")
            self.game.sound.register_sound('startmultiball', sound_path+"startmultiball1.wav")

            self.game.lampctrl.register_show('multiball_start', lampshow_path +"attract/wiekensnel.lampshow")
            self.game.lampctrl.register_show('jackpot_show', lampshow_path +"attract/rightleft.lampshow")

            self.lamps_trafficlight = ['stoplight_green','stoplight_yellow','stoplight_red']
            self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']
            self.lamps_center = ['detourWL','Cextraball','spotLetter']

            self.jackpot_status='jackpot_lit'
            self.timelock='on'
            # Steven:
            self.restart=True
            self.no_eject=False
            #self.jackpot_value = 1000000 # VIA MENU
            #self.superjackpot_value = 2500000 # VIA MENU
            self.jackpot_setting = 1000000 # VIA MENU
            self.superjackpot_setting = 2500000 # VIA MENU
            #self.mball_restart_time = 10 # VIA MENU
            self.mball_restart_time = self.game.user_settings['Gameplay (Feature)']['Multiball Restart Time']
            self.multiball_score=0

        def mode_started(self):
            print("Debug, Multibastard Mode Started")
            self.game.set_player_stats('multiball_running',True)
            # start multiball intro
            self.multiball_intro()


        def mode_stopped(self):
            print("Debug, Multibastard Mode Stopped")
            self.game.set_player_stats('multiball_running',False)
            self.game.set_player_stats('multiball_score',self.multiball_score)
            self.clear_lamps()
            self.clear_layer()
            self.game.effects.eject_ball()
            print('number balls in play = ', self.game.trough.num_balls_in_play)

## lamps & animations

        def update_lamps(self):
            if self.game.trough.num_balls_in_play==3:
                self.game.effects.drive_lamp('allScoresDouble','medium')
            else:
                self.game.effects.drive_lamp('allScoresDouble','off')

            # update lamps for jackpot
            if self.jackpot_status=='jackpot_lit':
                self.game.lamps.Clock.disable()
                self.game.lamps.Llock.disable()
                # update lamps right ramp
                self.game.lamps.megaScore.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                self.game.lamps.Rtimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                self.game.lamps.Rlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=True)
                self.game.lamps.Rextraball.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                # update trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'medium')
                # update lamps center
                for i in range(len(self.lamps_center)):
                     self.game.effects.drive_lamp(self.lamps_center[i],'off')

            # update lamps for superjackpot
            elif self.jackpot_status=='superjackpot_lit':
                self.game.lamps.Llock.disable()
                # update lamps right ramp
                for i in range(len(self.lamps_ramp)):
                     self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
                # update lamps trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')
                # update lamps center ramp
                self.game.lamps.detourWL.schedule(schedule=0x00ffff00, cycle_seconds=0, now=True)
                self.game.lamps.Cextraball.schedule(schedule=0x000ffff0, cycle_seconds=0, now=True)
                self.game.lamps.spotLetter.schedule(schedule=0x0000ffff, cycle_seconds=0, now=True)

            # update lamps for after jackpot or superjackpot
            elif self.jackpot_status=='jackpot_done' or self.jackpot_status=='superjackpot_done':
                self.game.effects.drive_lamp('Llock','medium')
                # update lamps right ramp
                for i in range(len(self.lamps_ramp)):
                     self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
                # update lamps center
                for i in range(len(self.lamps_center)):
                     self.game.effects.drive_lamp(self.lamps_center[i],'off')
                # update trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')

            # update lamps for timelocks
            if self.timelock=='on':
                self.game.lamps.Ltimelock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=False)
                self.game.lamps.Ctimelock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=False)
            elif self.timelock=='off': #and not self.jackpot_status==0
                self.game.effects.drive_lamp('Ltimelock','off')
                self.game.effects.drive_lamp('Ctimelock','off')
                if self.restart=='on':
                     self.game.effects.drive_lamp('Ltimelock','fast')   

        def clear_lamps(self):
            for i in range(len(self.lamps_ramp)):
                     self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
            for i in range(len(self.lamps_center)):
                self.game.effects.drive_lamp(self.lamps_center[i],'off')
            for i in range(len(self.lamps_trafficlight)):
                self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')
            self.game.effects.drive_lamp('Ltimelock','off')
            self.game.effects.drive_lamp('Ctimelock','off')
            self.game.effects.drive_lamp('Llock','off')
            # update lamps for entire game
            self.game.update_lamps()

        def multiball_animation(self):
             anim = dmd.Animation().load(dmd_path+"rk_mball_start.dmd")
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True,frame_time=4)
             #self.animation_layer.add_frame_listener(-1, self.start_multiball)
             self.layer=self.animation_layer
             #self.layer=dmd.GroupedLayer(128,32,[self.animation_layer])
             self.delay(name='start_multiball', event_type=None, delay=7, handler=self.start_multiball)
             #self.delay(name='clear_layer', event_type=None, delay=8, handler=self.clear_layer)

        def jackpot_animation(self, award):
             if award == 'jackpot':
                  anim = dmd.Animation().load(dmd_path+"nf_jackpot.dmd")
             elif award == 'superjackpot':
                  anim = dmd.Animation().load(dmd_path+"nf_superjackpot.dmd")
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False,frame_time=4)
             self.animation_layer.add_frame_listener(-1, self.show_jackpot_value)
             self.layer=dmd.GroupedLayer(128,32,[self.animation_layer])

        def show_jackpot_value(self):
             if self.jackpot_status=='superjackpot_lit':
                    self.value_layer.set_text(" SUPERJACKPOT: "+str(locale.format("%d", self.superjackpot_value, True)+" "))
             else: #begin en end with withspaces to overwrite 'Ball 1 free play' line
                    self.value_layer.set_text("  JACKPOT: "+str(locale.format("%d", self.jackpot_value, True)+"  "))
             self.layer = self.value_layer

        def totalscore_animation(self):
             self.score_layer.set_text(locale.format("%d", self.multiball_score, True))
             self.mbtotal_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mb_total.dmd').frames[0])
             self.layer=dmd.GroupedLayer(128,32,[self.mbtotal_layer,self.score_layer])

        def clear_layer(self):
            self.layer = None

        def gi_blink(self):
            self.game.effects.gi_blinking(schedule=33333333, cycle_seconds=2)

## mode functions

        def multiball_intro(self):
            self.game.sound.play('startmultiball')
            self.game.effects.gi_blinking(cycle_seconds=2)
            # delay animation to synchronise with sound
            self.delay(name='multiball_animation', event_type=None, delay=1, handler=self.multiball_animation)
            #play lightshow
            self.game.lampctrl.play_show('multiball_start', True, 'None')
            # delay gi to synchronise with animation
            self.delay(name='gi_blink', event_type=None, delay=7, handler=self.gi_blink)

        def start_multiball(self):
             #setup  multiball
             self.multiball_running = True
             self.jackpot_status='jackpot_lit'
             #launch ball
             self.game.trough.launch_balls(1)
             #play music
             self.game.sound.play_music('multiball_theme', loops=-1)
             #put ramp down
             self.game.base_game_mode.rampmove.move_ramp('down')
             #stop lightshow
             self.game.lampctrl.stop_show()
             #update lamps for entire game after lampshow
             self.delay(name='update_lamps', event_type=None, delay=1, handler=self.game.update_lamps)
             self.update_jackpot()

        def multiball_restart(self):
             #self.delay(name='stopmultiball', event_type=None, delay=self.mball_restart_time, handler=self.stop_multiball)
             self.game.sound.fadeout_music()
             self.counter = self.mball_restart_time
             #self.game.sound.play_music('clock_ticking', loops=0)
             self.start_countdown()
             self.play_countdown()
             #Steven
             self.restart='on'
             self.timelock='off'
             self.cancel_delayed('kickout_Ceject')
             self.cancel_delayed('kickout_Leject')
             if not self.no_eject:
                self.game.effects.eject_ball(location='all')
             self.update_lamps()
             

        def start_countdown(self):
            #Countdown via repeated call to itself with delaytime 1sec, if time is up, stop and remove mode
            if self.counter == 0:
                self.stop_multiball()
            else:
                self.delay(name='start_countdown', event_type=None, delay=1, handler=self.start_countdown)
                self.game.effects.gi_blinking(schedule=0x00FF00FF, cycle_seconds=1)
            # set counter value on textlayer
            self.timer_layer.set_text(str(self.counter))
            # decrease counter
            self.counter -=1

        def clear_countdown(self):
             #clear countdown
             self.cancel_delayed('start_countdown')
             #self.clear_layer()
             #self.game.sound.stop_music()

        def play_countdown(self):
             self.title_layer.set_text('RESTART M-BALL')
             anim = dmd.Animation().load(dmd_path+'mball_restart.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=2)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.timer_layer])

        def stop_multiball(self):
             self.clear_layer()
             self.callback('multibastard')

        def update_jackpot(self):
             if self.game.trough.num_balls_in_play == 3:
                  self.jackpot_value = self.jackpot_setting * 2
                  self.superjackpot_value = self.superjackpot_setting * 2
             else:
                  self.jackpot_value = self.jackpot_setting
                  self.superjackpot_value = self.superjackpot_setting
             print("jackpotvalue = ", self.jackpot_value)
             print("superjackpotvalue = ", self.superjackpot_value)
             self.show_jackpot_value()

        def jackpot(self):
            # play sound, animation and lightshow
            self.game.sound.play('jackpot')
            self.jackpot_animation('jackpot')
            self.game.lampctrl.play_show('jackpot_show', False, 'None')
            # set jackpot status
            self.jackpot_status='jackpot_done'
            # calculate score
            self.game.score(self.jackpot_value)
            self.multiball_score+=self.jackpot_value
            # update lamps after lightshow
            self.delay(name='update_lamps', event_type=None, delay=3, handler=self.game.update_lamps)

        def superjackpot(self):
            # play sound, animation and lightshow
            self.game.sound.play('superjackpot')
            self.jackpot_animation('superjackpot')
            self.game.lampctrl.play_show('jackpot_show', False, 'None')
            # set jackpot status
            self.jackpot_status='superjackpot_done'
            # calculate score
            self.game.score(self.superjackpot_value)
            self.multiball_score+=self.superjackpot_value
            # update lamps after lightshow
            self.delay(name='update_lamps', event_type=None, delay=3, handler=self.game.update_lamps)

        def eject_active(self, ejecthole):
            #Steven
            if self.no_eject:
                self.no_eject=False
            elif self.timelock=='on':
                self.delay(name='kickout_'+ejecthole, event_type=None, delay=8, handler=self.kickout_eject, param=ejecthole)
                self.timelock='ball_captured'
                self.game.sound.play('ball1locked')
                if ejecthole == 'Ceject':
                   self.game.lamps.Ctimelock.enable()
                else:
                   self.game.lamps.Ltimelock.enable()
            elif self.timelock=='ball_captured':
                if ejecthole == 'Ceject':
                   self.cancel_delayed('kickout_Leject')
                else:
                   self.cancel_delayed('kickout_Ceject')
                self.game.sound.play('ball2locked')
                self.game.score(50000)
                self.game.trough.launch_balls(1)
                self.timelock='off'
            else:
                self.game.effects.eject_ball(location=ejecthole)
            self.update_jackpot()
            self.update_lamps()

        def kickout_eject(self, ejecthole):
            self.game.coils[ejecthole].pulse(18)
            self.timelock='on'
            self.update_lamps()

        def bumper(self):
             self.game.score(10)
             self.game.sound.play('bumper')

## switches

        def sw_Ceject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_Ceject_active_for_600ms(self,sw):
             self.eject_active('Ceject')

        def sw_Leject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_Leject_active_for_600ms(self,sw):
             if self.jackpot_status=='jackpot_done':
                 self.jackpot_status='superjackpot_lit'
                 self.game.effects.raise_droptarget()
             elif self.jackpot_status=='superjackpot_done':
                   self.jackpot_status='jackpot_lit'
                   self.game.sound.play('jackpotislit')
             #Steven
             elif self.restart=='on':
                   self.restart=False
                   self.clear_countdown()
                   self.timelock='on'
                   self.multiball_intro()
                   self.no_eject=True
             self.update_jackpot()
             self.eject_active('Leject')

        def sw_upperLkicker_active(self, sw):
            self.delay(name='ulkicker', event_type=None, delay=2, handler=self.game.effects.eject_ball, param='upperLkicker')
            return procgame.game.SwitchStop

        def sw_RrampExit_active(self, sw):
            if self.jackpot_status=='jackpot_lit':
                self.jackpot()
            return procgame.game.SwitchStop

        def sw_dropTarget_active(self,sw):
            if self.jackpot_status=='superjackpot_lit':
                self.game.sound.play('superjackpotislit')

        def sw_CrampEnter_active(self,sw):
            if self.jackpot_status=='superjackpot_lit':
                self.superjackpot()
                # Do not pass switch to other modes if jackpot is scored
                return procgame.game.SwitchStop

        def sw_bumperL_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperU_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperR_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperD_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop
            
        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_1s(self,sw):
             self.game.effects.eject_ball(location='all')
             self.update_lamps()

        def sw_Lspinner_active(self, sw):
            return procgame.game.SwitchStop

        # check whether allscoresdouble end or end mode when a ball drains
        def sw_outhole_active(self,sw):
            print('number balls in play=', self.game.trough.num_balls_in_play)
            if self.game.trough.num_balls_in_play==3:
                self.game.effects.drive_lamp('allScoresDouble','off')
            if self.game.trough.num_balls_in_play==2:
                 if self.multiball_score == 0 and self.restart==True:
                     #Steven
                     #self.jackpot_status='multiball_restart'
                     self.restart='on'
                     self.multiball_restart()
                 else:
                     # grace period 
                     self.delay(name='stopmultiball', event_type=None, delay=2.5, handler=self.stop_multiball)
                     self.clear_countdown()
                     self.totalscore_animation()
            # update jackpot when ball is in trough
            self.delay(name='update_jackpot', event_type=None, delay=1, handler=self.update_jackpot)
            #self.update_jackpot()
