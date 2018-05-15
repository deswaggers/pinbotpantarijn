# Mode bumpers
import procgame
from procgame import *
import locale
import random

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path + "sound/speech/"
sound_path = game_path + "sound/fx/"
music_path = game_path + "sound/music/"
dmd_path = game_path + "dmd/"
lampshow_path = game_path +"lampshows/"


class RampMultiball(game.Mode):
    def __init__(self, game, priority):
        super(RampMultiball, self).__init__(game, priority)

    def mode_started(self):
        print "RampMultiball uit ramp_multiball.py is gestart"
        self.instruction_layer = dmd.TextLayer(30, 20, self.game.fonts['num_14x10'], opaque=False)
        #self.game.lampctrl.register_show('multiball_start', lampshow_path +"planeten_short.lampshow")
        #self.game.lampctrl.register_show('visor_lampshow', lampshow_path +"Pinbot_1.lampshow")
        self.delay(name='start_rampMB', event_type=None, delay=5, handler=self.start_rampMB)
        self.display_instructions()
        self.twoballsinplay = False


    def start_rampMB(self):
        print "nu is start_rampMB gestart, dus moet ie een bal geven"
        self.game.trough.launch_balls(1)
        self.game.sound.play_music('music_harp', loops=-1)


    def mode_tick(self):
        if ((self.game.trough.num_balls_in_play<2) and self.twoballsinplay):
            self.stop_rampmultiball()


    def stop_rampmultiball(self):
        self.game.sound.play_music('music_2017_creepy_alien_music')
        self.game.modes.remove(self)
        self.layer = None


    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

    def display_instructions(self):
        self.instruction_layer.set_text('RAMP MULTIBALL GESTART')
        self.layer=dmd.GroupedLayer(128,32,[self.instruction_layer])


    def sw_shooterLane_open_for_500ms(self,sw):
        self.game.coils.RvisorGI.schedule(schedule=0x0f0f0f0f, cycle_seconds=2, now=True)
        self.game.coils.LvisorGI.schedule(schedule=0xf0f0f0f0, cycle_seconds=2, now=True)
        self.game.effects.ramp_up()
        self.twoballsinplay = True


    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
