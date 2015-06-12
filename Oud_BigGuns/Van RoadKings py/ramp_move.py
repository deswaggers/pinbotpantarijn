#
# Ramp move
#
# Game mode that controls movement of the rightramp entrance
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
import logging
from procgame import *

#all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"


class Rampmove(game.Mode):

        def __init__(self, game, priority):
            super(Rampmove, self).__init__(game, priority)

            self.log = logging.getLogger('rk.Rampmove')
            self.game.sound.register_sound('ramp_change', sound_path+"rampchange2.aiff")

            self.text_layer = dmd.TextLayer(70, 22, self.game.fonts['07x5'], "center", opaque=False).set_text("MOVE RAMP", blink_frames=10)
            self.workshop_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'workshop.dmd').frames[0])
            self.workshop_layer = dmd.GroupedLayer(128, 32, [self.workshop_bgnd, self.text_layer])
            self.workshop_layer.transition = dmd.PushTransition(direction='north')

            self.ramp_up = False

        def reset(self):
            pass

        def mode_started(self):
            print("Debug, Rampmove Mode Started")
            self.check_state()

        def mode_stopped(self):
            print("Debug, Rampmove Mode Ended")
            self.move_ramp('down')

        def mode_tick(self):
            pass

## mode functions

        def play_animation(self):
            script = list()
            script.append({'seconds':2.0, 'layer':self.workshop_layer})
            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def clear_layer(self):
             self.layer = None

        def check_state(self):
            if self.game.switches.rampRaise.is_active():
                self.ramp_up = False;
                print("Ramp= Down")
            elif self.game.switches.rampRaise.is_inactive():
                self.ramp_up = True;
                print("Ramp= Up")
            self.game.set_player_stats('ramp_state',self.ramp_up)
            # update lamp status's for all modes in case of ramp change
            self.game.effects.update_ramp_lamps()
            return self.ramp_up

        def move_ramp(self,direction='down'):
           #rampup and rampdown procedure:
           #To make sure the rampstate has changed, a repeated call to
           #itself is made to check the change in switch rampRaise

           if direction=='down':
                #cancel previous check if direction changes
                self.cancel_delayed('rampupcheck')

                if self.game.switches.rampRaise.is_inactive():
                    #activate ACSelect + coil
                    self.game.coils.ACselect.pulse(50)
                    self.game.coils.midBikeFlash_rampDown.pulse(40)
                    #play sound
                    self.game.sound.play('ramp_change')
                    #repeat call after delay to check change
                    self.delay(name='rampdowncheck', event_type=None, delay=1, handler=self.move_ramp, param='down')


           elif direction=='up':
                #cancel previous check if direction changes
                self.cancel_delayed('rampdowncheck')

                if self.game.switches.rampRaise.is_active():
                    #activate ACSelect + coil
                    self.game.coils.ACselect.pulse(60)
                    self.game.coils.knocker_rampUp.pulse(50)
                    #play sound
                    self.game.sound.play('ramp_change')
                    #repeat call after delay to check change
                    self.delay(name='rampupcheck', event_type=None, delay=1, handler=self.move_ramp, param='up')

           else:
                print ("rampdirection unclear: "+str(direction))

           self.delay(name='check_state', event_type=None, delay=1, handler=self.check_state)

## switches

        def sw_Leject_active_for_200ms(self, sw):
            self.play_animation()
            self.game.coils.Rlightningbolt.schedule(33333333, cycle_seconds=1, now=True)

        def sw_Leject_active_for_500ms(self, sw):
            if self.game.switches.rampRaise.is_inactive():
                self.move_ramp('down')
            elif self.game.switches.rampRaise.is_active():
                  self.move_ramp('up')


