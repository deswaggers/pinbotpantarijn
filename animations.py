# Effects
#
# Basic mode for general effects and control of game items (lamps, coils, etc.)

import procgame
import locale
from procgame import *
import time

game_path = game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Animations(game.Mode):

    def __init__(self, game):
        super(Animations, self).__init__(game, 4)
        self.game.sound.register_sound('ramp_up', sound_path+"rampup.wav")
        self.text_layer = dmd.TextLayer(4, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.text_layer.set_text("",True)

    def astronaut(self):
        #self.game.sound.play('speech_welcome')
        self.animation_layer = dmd.AnimatedLayer(frames=dmd.Animation().load(dmd_path+'astronaut.dmd').frames, opaque=False, repeat=False, hold=False, frame_time=1)
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
        self.delay(name='clear_layer', event_type=None, delay=4, handler=self.clear_layer)

    def space_pinball_welcome(self, cleartime=2):
        self.game.sound.play("sound_2017_launch_flight")
        self.space_pinball = dmd.AnimatedLayer(frames=dmd.Animation().load(game_path+'dmd/welcome_space_pinball.dmd').frames, opaque=False, repeat=True, hold=False, frame_time=3))
        self.layer = dmd.GroupedLayer(128, 32, [self.space_pinball,self.text_layer])
        self.delay(name='clearLayer', event_type=None, delay=cleartime, handler=self.clear_layer)

    def space_ship_flies(self, cleartime=2):
        self.game.sound.play("sound_rocket-launch")
        self.animation_layer = dmd.AnimatedLayer(frames=dmd.Animation().load(dmd_path+'ruimteschip.dmd').frames, opaque=False, repeat=False, hold=False, frame_time=8)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
        self.delay(name='clearLayer', event_type=None, delay=cleartime, handler=self.clear_layer)

    def space_ship_shoots(self, score=100, cleartime=1):
        self.text_layer.set_text(str(score)+ "POINTS",True)
        self.game.sound.play("sound_2017_lasershot")
        self.animation_layer = dmd.AnimatedLayer(frames=dmd.Animation().load(dmd_path+'schietende_raket_2frames.dmd').frames, opaque=False, repeat=True, hold=False, frame_time=10)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.text_layer])
        self.delay(name='clearLayer', event_type=None, delay=cleartime, handler=self.clear_layer)

    def space_ship_crashes(self, score=100, cleartime=4):
        self.text_layer.set_text(str(score),True)
        self.game.sound.play("sound_2017_explosion")
        self.animation_layer = dmd.AnimatedLayer(frames=dmd.Animation().load(dmd_path+'neerstortende_raket_25frames.dmd').frames, opaque=False, repeat=False, hold=True, frame_time=5)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.text_layer])
        self.delay(name='clearLayer', event_type=None, delay=cleartime, handler=self.clear_layer)

    def space_ship_leaves(self, score=100, cleartime=4):
        self.text_layer.set_text(str(score)+"POINTS",True)
        self.game.sound.play("sound_2017_one_step_for_man")
        self.animation_layer = dmd.AnimatedLayer(frames=dmd.Animation().load(dmd_path+'vertrekkende_raket_langs_planeet_22frames.dmd').frames, opaque=False, repeat=False, hold=False, frame_time=8)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.text_layer])
        self.delay(name='clearLayer', event_type=None, delay=cleartime, handler=self.clear_layer)

    def saturnus(self, score=100):
        self.text_layer = dmd.TextLayer(26, 80, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.text_layer.set_text(str(score)+"POINTS",True)
        anim = dmd.Animation().load(dmd_path+'saturnusbmp.dmd')
        self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=8)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.text_layer])
        self.text_layer = dmd.TextLayer(4, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)

    def clear_layer(self):
        self.layer = None
        self.text_layer.set_text("",True)