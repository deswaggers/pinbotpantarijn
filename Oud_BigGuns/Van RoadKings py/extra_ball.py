#
# Extra Ball
#
# Control of extra ball 
# 
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"

import procgame
import locale
from procgame import *

game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
lampshow_path = game_path +"lampshows/"

class Extra_Ball(game.Mode):

        def __init__(self, game):
            super(Extra_Ball, self).__init__(game, 90)

            self.game.sound.register_sound('extra_ball_collected', sound_path+"extra_ball.wav")
            self.game.sound.register_sound('extra_ball_lit', speech_path+"extra_ball_lit.wav")
            self.game.sound.register_sound('extra_ball_hurryup', speech_path+"extra_ball_hurryup.wav")

            self.game.lampctrl.register_show('succes', lampshow_path+"succes.lampshow")

            #self.extraball_menu = True # VIA MENU
            self.extraball_menu = self.game.user_settings['Gameplay (Feature)']['Extraball Awarded']

        def clear_layer(self):
            self.layer = None

        def reset_xball(self):
            self.game.set_player_stats('extraball_on', False)

        def collect(self, location='Rextraball'):
            self.cancel_delayed('reset_xball')
            anim = dmd.Animation().load(game_path+"dmd/jd_extra_ball.dmd")
            self.layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True,frame_time=4)
            self.game.sound.play('extra_ball_collected')
            #self.game.sound.play_voice('extra_ball_speech')
            self.game.effects.drive_lamp(location,'off')
            self.game.lampctrl.play_show('succes', False, 'None')
            if self.extraball_menu:  # Menu instelling voor extraball of score
                self.game.effects.drive_lamp('cruiseAgain','smarton')
                self.game.extra_ball_count()
            else: 
                self.game.score(5000000)
            self.reset_xball()
            self.delay(name='clear_layer', event_type=None, delay=4, handler=self.clear_layer)

        def lit(self, location='Rextraball'):
            self.game.sound.play('extra_ball_lit')
            self.game.set_player_stats('extraball_on', True)
            self.game.effects.drive_lamp(location,'smarton')

        def hurryup(self, location='Rextraball'):
            self.game.sound.play('extra_ball_lit')
            self.game.set_player_stats('extraball_on', True)
            self.game.effects.drive_lamp(location,'timeout',time=30)
            self.delay(name='reset_xball', event_type=None, delay=31, handler=self.reset_xball)
            self.game.sound.play_voice('extra_ball_hurryup')
