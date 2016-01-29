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


class Mode5(game.Mode):
    def __init__(self, game, priority):
        super(Mode5, self).__init__(game, priority)

    def mode_started(self):
        self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
        self.raise_layer = dmd.TextLayer(5, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.flashers = ["RampLow_EnergyFlash", "Lejecthole_LeftPlFlash", "Rejecthole_SunFlash"]
        self.flasher_list = ["Lejecthole_LeftPlFlash", "Ejecthole_LeftInsBFlash", "Drops_RightInsBFlash"]
        ## eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
        self.delay(name='Mode_start_na_eject', event_type=None, delay=2, handler=self.mode_start_na_eject)
        self.delay(name='flasher_delay', event_type=None, delay=3, handler=self.flasher_drive)
        self.rampexit_counter = 0
        self.lamplist = ["2x", "3x", "4x", "5x"]
        self.x = 1764
        self.game.effects.drive_lamp('solar_energy', 'fast')

    def mode_start_na_eject(self):
        self.game.effects.eject_ball('eject')
        self.game.sound.play_music('music_doctorwho', loops=-1)

    def mode_stopped(self):
        print "mode 5 afgesloten"
        self.game.effects.drive_lamp('solar_energy', 'off')
        
        if self.rampexit_counter > 3:
            self.game.score(self.x * self.rampexit_counter * (self.rampexit_counter - 2))
        else:
            self.game.score(self.x * self.rampexit_counter)
        for i in self.lamplist:
            self.game.effects.drive_lamp(i, "off")
        self.game.sound.play_music('music_hitchhiker', loops=-1)
        self.layer = None
        self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

    def sw_rampexit_active(self, sw):
        for i in self.flashers:
            self.game.switchedCoils.acFlashPulse(i, 255)
        self.game.sound.play('sound_bleep05') #bleep05 is ook wel leuk
        if self.rampexit_counter == 5:
            self.game.current_player().stop_eject_mode_mode(self)
        else:
            self.rampexit_counter += 1
            self.update_lamps()
            self.game.score(2016)
            
    def sw_outhole_active(self, sw):
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
        
    def update_lamps(self):
        if self.rampexit_counter == 5:
            self.game.effects.drive_lamp(self.lamplist[self.rampexit_counter - 2], 'on')
        
        elif self.rampexit_counter > 1:
            self.game.effects.drive_lamp(self.lamplist[self.rampexit_counter - 1], 'fast')
            self.game.effects.drive_lamp(self.lamplist[self.rampexit_counter - 2], 'on')
        elif self.rampexit_counter == 1:
            self.game.effects.drive_lamp(self.lamplist[self.rampexit_counter - 1], 'fast')
        else:
            pass


    def flasher_drive(self):
        for i in self.flasher_list:
            self.game.switchedCoils.acFlashPulse(i, 255)
        self.delay(name='flasher_delay', event_type=None, delay=4, handler=self.flasher_drive)
