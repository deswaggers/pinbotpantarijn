#
# Race Champion mode
#
# Main game mode (1 of 4) 
# Shoot lit shot progresses race, not shooting the lit shot makes it go back 'one step' 
# 

__author__="Steven"
__date__ ="$19 Nov 2012 15:21:12 PM$"

from procgame import *
import locale

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Racechampion(game.Mode):
        def __init__(self, game, priority):
                super(Racechampion, self).__init__(game, priority)
                self.game.sound.register_sound('bumper', sound_path+"bumpers.aiff")
                self.game.sound.register_sound('shot_made', speech_path+"rc_.ogg")

                self.game.sound.register_music('racechampion_theme', music_path+"racechampion.ogg")

                self.game.lampctrl.register_show('shotmade', lampshow_path+"rc_shotmade.lampshow")

                self.title_layer = dmd.TextLayer(128/2, 2, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10
                #self.score_layer = dmd.TextLayer(128/2, 21, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.score_layer = dmd.TextLayer(128/2, 17, self.game.fonts['num_14x10'], "center", opaque=True)

                self.shot='middle'
                self.left_saucer=0
                self.centre_ramp=0
                self.centre_saucer=0
                self.right_loop=0
                self.road_targets=0
                self.kings_targets=0

                self.racedone=False
                self.time_left=16
                self.timer_setting = 15
                #self.timer_setting = self.game.user_settings['Gameplay (Feature)']['Easy Rider Timer']
                self.fase='fase1'
                self.shot_value = 250000
                self.jackpot_value = 2500000

                self.lamps_trafficlight = ['stoplight_green','stoplight_yellow','stoplight_red']
                self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']
                self.lamps_road = ['targetR','targetO','targetA','targetD']
                self.lamps_kings = ['targetK','targetI','targetN', 'targetG','targetS']

                #self.knocker_on = False # VIA MENU
                self.knocker_on = self.game.user_settings['Gameplay (Feature)']['Easy Rider Knocker On']

                self.Lroll=0

        def mode_started(self):
                print("Debug, Easyrider Mode Started")
                self.game.sound.play_music('easyrider_theme', loops=-1)
                self.game.base_game_mode.rampmove.move_ramp('up')
                for lamp in self.game.lamps:
                        lamp.disable()
                self.start_easyrider()
                self.play_animation()
                self.update_lamps_easyrider()

        def mode_stopped(self):
                print("Debug, Easyrider Mode Stopped")
                self.cancel_delayed('kickout_Cejecthole')
                self.cancel_delayed('kickout_Lejecthole')
                for lamp in self.game.lamps:
                        lamp.disable()
                self.game.base_game_mode.rampmove.move_ramp('down')
                self.layer=None

        def start_easyrider(self):
                #self.delay(name='rollreset', event_type=None, delay=1.9, handler=self.rollreset)
                #self.delay(name='rollreset2', event_type=None, delay=3.8, handler=self.rollreset)
                #self.game.sound.play('loops')
                self.game.effects.eject_ball('upperLkicker')
                self.countdown()

        def mode_tick(self):
                pass

## lamps & animations

        def update_lamps_easyrider(self):
                for lamp in self.game.lamps:
                        lamp.disable()

                if self.fase=='fase2':
                        for i in range(len(self.lamps_road)):
                                self.game.effects.drive_lamp(self.lamps_ramp[i],'medium')
                        for i in range(len(self.lamps_trafficlight)):
                                self.game.effects.drive_lamp(self.lamps_trafficlight[i],'fast')
                else:
                        for i in range(len(self.lamps_road)):
                                self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
                        for i in range(len(self.lamps_trafficlight)):
                                self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')

                if self.spinner==0:
                        self.game.lamps.bonusholdWL.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                else:
                        self.game.lamps.bonusholdWL.enable()
                if self.left_saucer==0:
                        self.game.lamps.Ltimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                else:
                        self.game.lamps.Ltimelock.enable()
                if self.centre_ramp==0:
                        self.game.lamps.detourWL.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                else:
                        self.game.lamps.detourWL.enable()
                if self.centre_saucer==0:
                        self.game.lamps.Ctimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                else:
                        self.game.lamps.Ctimelock.enable()
                if self.right_loop==0:
                        self.game.lamps.Rtimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                else:
                        self.game.lamps.Rtimelock.enable()
                if self.kings_targets==0:
                        for i in range(len(self.lamps_kings)):
                                self.game.effects.drive_lamp(self.lamps_kings[i],'medium')
                else:
                        for i in range(len(self.lamps_kings)):
                                self.game.effects.drive_lamp(self.lamps_kings[i],'on')
                if self.road_targets==0:
                        for i in range(len(self.lamps_road)):
                                self.game.effects.drive_lamp(self.lamps_road[i],'medium')
                else:
                        for i in range(len(self.lamps_road)):
                                self.game.effects.drive_lamp(self.lamps_road[i],'on')

        def play_animation(self):
            #if self.animation_status=='ready':
              anim = dmd.Animation().load(dmd_path+'easy_rider.dmd')
              self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=6)
              self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.score_layer])

        def clear_layer(self):
             self.layer = None

## mode functions

        def check_road(self):
                if self.road_targets==0:
                        self.road_targets=1
                        self.time_left=self.timer_setting
                        self.update_status()

        def check_kings(self):
                if self.kings_targets==0:
                        self.kings_targets=1
                        self.time_left=self.timer_setting
                        self.update_status()

        def knock_times(self, param=1):
             if self.knocker_on:
                  if param >=1:
                       self.delay(name='knocker', event_type=None, delay=0.4, handler=self.knocker)
                  if param >=2:
                       self.delay(name='knocker', event_type=None, delay=0.8, handler=self.knocker)
                  if param >=3:
                       self.delay(name='knocker', event_type=None, delay=1.2, handler=self.knocker)
                  if param >=4:
                       self.delay(name='knocker', event_type=None, delay=1.6, handler=self.knocker)
                  if param >=5:
                       self.delay(name='knocker', event_type=None, delay=2.0, handler=self.knocker)
                  if param >=6:
                       self.delay(name='knocker', event_type=None, delay=2.4, handler=self.knocker)
                  if param >=7:
                       self.delay(name='knocker', event_type=None, delay=2.8, handler=self.knocker)

        def knocker(self):
                self.game.coils.knocker_rampUp.pulse(9)

        def check_shots_made(self):
             shots_made = self.spinner+self.left_saucer+self.centre_ramp+self.centre_saucer+self.right_loop+self.road_targets+self.kings_targets
             return shots_made

        def shot_made(self):
             self.game.sound.play('shot_made')
             self.game.lampctrl.play_show('shotmade', False, 'None')
             self.game.score(self.shot_value)
             self.score_layer.set_text(locale.format("%d",self.shot_value, True), seconds=2, blink_frames=2)
             #self.knock_times(param)

        def update_status(self):
                if self.check_shots_made() == 1:
                        self.knock_times(1)
                        #self.game.sound.play('loops')
                        self.shot_made()
                elif self.check_shots_made() == 2:
                        self.knock_times(2)
                        #self.game.sound.play('flashing target')
                        self.shot_made()
                elif self.check_shots_made() == 3:
                        self.knock_times(3)
                        self.shot_made()
                elif self.check_shots_made() == 4:
                        self.knock_times(4)
                        #self.game.sound.play('flashing target')
                        self.shot_made()
                elif self.check_shots_made() == 5:
                        self.knock_times(5)
                        self.shot_made()
                elif self.check_shots_made() == 6:
                        self.knock_times(6)
                        self.shot_made()
                elif self.check_shots_made() == 7 and self.fase=='fase1':
                        self.shot_made()
                        self.game.base_game_mode.rampmove.move_ramp('down')
                        self.fase='fase2'
                        self.delay(name='shootrampsound', event_type=None, delay=3, handler=self.shootrampsound)
                        self.knock_times(7)
                if self.racedone==True:
                        self.racedone=False
                        self.game.coils.flipperEnable.enable()
                        self.game.effects.gi_on()
                        self.title_layer.set_text('BACK ON TRACK..')
                        self.delay(name='countdown', event_type=None, delay=2, handler=self.countdown)
                        self.game.ball_save.start(num_balls_to_save=1, time=8, now=True, allow_multiple_saves=False)
                self.update_lamps_easyrider()

        def countdown(self):
                self.title_layer.set_text('TIME: '+str(self.time_left),True)
                self.time_left-=1
                self.delay(name='countdown', event_type=None, delay=1, handler=self.countdown)
                if self.time_left<0:
                        self.game.coils.flipperEnable.disable()
                        self.game.effects.gi_off()
                        self.racedone=True
                        self.cancel_delayed('countdown')
                        self.title_layer.set_text('RACE OVER...',4,4)
                        self.game.ball_save.start(num_balls_to_save=1, time=8, now=True, allow_multiple_saves=False)
                elif self.time_left==7:
                        self.game.sound.play('siren')
                elif self.time_left>6:
                        self.game.sound.stop('siren')

        def shootrampsound(self):
                #self.show_on_display('Shoot the ramp!','None','mid')
                self.game.sound.play('right ramp')

        def bumper(self):
                self.game.score(10)
                self.game.sound.play('bumper')

        def rollreset(self):
                self.Lroll=1

        def stop_easyrider(self):
                self.callback('racechampion')

## switches

        def sw_RrampExit_active(self,sw):
                if self.fase=='fase2':
                        self.game.sound.play('easy_rider_jp')
                        self.fase='fase3'
                        self.cancel_delayed('countdown')
                        self.title_layer.set_text('THATS EASY RIDING') #EASY GOING RIDER, THATS EASY RIDING, YOU R EASY RIDING
                        self.score_layer.set_text(locale.format("%d",self.jackpot_value, True), seconds=3, blink_frames=2)
                        self.game.sound.play('thatseasy')
                        for lamp in self.game.lamps:
                                lamp.disable()
                        self.game.coils.GIrelay.schedule(schedule=0xffffffff, cycle_seconds=0, now=False)
                        self.game.coils.Rlightningbolt.schedule(0x50505050, cycle_seconds=4, now=False)
                        self.game.coils.Llightningbolt.schedule(0x05050505, cycle_seconds=4, now=False)
                        self.game.coils.bikesFlash_dropTarget.schedule(0x04040404, cycle_seconds=4, now=False)
                        self.game.coils.midBikeFlash_rampDown.schedule(0x03030303, cycle_seconds=4, now=False)
                        self.game.coils.rearFlash_upLeftkicker.schedule(0x03030303, cycle_seconds=4, now=False)
                        self.knock_times(7)
                        self.game.ball_save.start(num_balls_to_save=1, time=15, now=True, allow_multiple_saves=False)
                        self.game.coils.flipperEnable.disable()
                        self.game.score(self.jackpot_value)
                        # display, ook 'je keert terug naar het normale spel: weer bal afschieten'
                        # geluid (inclusief uitleg)
                        # lichtshow
                self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=5, now=False)
                self.delay(name='kickoutupperLkicker', event_type=None, delay=3.5, handler=self.game.effects.eject_ball)
                return True

        def sw_Lspinner_active(self,sw):
                self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                if not self.game.switches.Rrollunder.time_since_change() < 1.5 and self.Lroll==1:
                        if self.spinner==0:
                                self.spinner=1
                                self.time_left=self.timer_setting
                                self.update_status()
                if self.game.switches.Rrollunder.time_since_change() < 1.5:
                        if self.right_loop==0:
                                self.right_loop=1
                                self.time_left=self.timer_setting
                                self.update_status()
                self.Lroll=0
                self.delay(name='rollreset', event_type=None, delay=2, handler=self.rollreset)
                return True

        def sw_Rrollunder_active(self,sw):
                self.game.coils.Lgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                return True

        def sw_Leject_active(self,sw):
                return True

        def sw_Leject_active_for_600ms(self,sw):
                if self.left_saucer==0:
                        self.delay(name='kickout_Lejecthole', event_type=None, delay=1.5, handler=self.game.effects.eject_ball)
                        self.left_saucer=1
                        self.time_left=self.timer_setting
                        self.update_status()
                else:
                        self.game.effects.eject_ball()
                return True


        def sw_CrampEnter_active(self,sw):
                if self.centre_ramp==0:
                        self.centre_ramp=1
                        self.time_left=self.timer_setting
                        self.update_status()
                return True
        def sw_CrampRexit_active(self,sw):
                return True
        def sw_Ceject_active(self,sw):
                return True
        def sw_Ceject_active_for_600ms(self,sw):
                if self.centre_saucer==0:
                        self.delay(name='kickout_Cejecthole', event_type=None, delay=1.5, handler=self.game.effects.eject_ball)
                        self.centre_saucer=1
                        self.time_left=self.timer_setting
                        self.update_status()
                else:
                        self.game.effects.eject_ball()
                return True

        def sw_outhole_active(self,sw):
                self.delay(name='stopracechampion', event_type=None, delay=1.0, handler=self.stop_racechampion)
                self.game.coils.flipperEnable.enable()
                self.game.effects.gi_on()
                self.game.sound.fadeout_music()

        def sw_targetR_active(self,sw):
                self.check_road()
                return True
        def sw_targetO_active(self,sw):
                self.check_road()
                return True
        def sw_targetA_active(self,sw):
                self.check_road()
                return True
        def sw_targetD_active(self,sw):
                self.check_road()
                return True
        def sw_targetK_active(self,sw):
                self.check_kings()
                return True
        def sw_targetI_active(self,sw):
                self.check_kings()
                return True
        def sw_targetN_active(self,sw):
                self.check_kings()
                return True
        def sw_targetG_active(self,sw):
                self.check_kings()
                return True
        def sw_targetS_active(self,sw):
                self.check_kings()
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
        def sw_slingL_active(self,sw):
                self.bumper()
                return True
        def sw_slingR_active(self,sw):
                self.bumper()
                return True
