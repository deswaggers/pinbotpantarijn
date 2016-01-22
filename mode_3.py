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


class Mode3(game.Mode):
    def __init__(self, game, priority):
        super(Mode3, self).__init__(game, priority)

        self.yellow = ["yellow1", "yellow2", "yellow3", "yellow4", "yellow5"]
        self.blue = ["blue1", "blue2", "blue3", "blue4", "blue5"]
        self.orange = ["orange1", "orange2", "orange3", "orange4", "orange5"]
        self.green = ["green1", "green2", "green3", "green4", "green5"]
        self.red = ["red1", "red2", "red3", "red4", "red5"]
        self.flashers = ["RampLow_EnergyFlash", "Lejecthole_LeftPlFlash", "Rejecthole_SunFlash"]
    def mode_started(self):
        self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
        self.raise_layer = dmd.TextLayer(5, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.delay(name='start_mode_delay', event_type=None, delay=1.5, handler=self.start_mode_delay)

        # Eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
        self.visor_count = 1
        self.visor_check()

    def start_mode_delay(self):
        self.game.effects.eject_ball('eject')

    def mode_stopped(self):
        self.game.sound.play_music('music_starwars_intro', loops=-1)
        self.game.current_player().set_mode_running(False)
        self.layer = None

    def final_flash(self):
        for i in (self.yellow + self.blue + self.orange + self.green + self.red):
            self.game.effects.drive_lamp(i, 'on')
       
        for i in self.flashers:
            self.game.switchedCoils.acFlashPulse(i, 255)
        self.game.effects.drive_flasher("TopFlash4", time=2, style="chaos")
        self.game.effects.drive_flasher("TopFlash3", time=2, style="strobe")
        self.game.effects.drive_flasher("RobotFaceInsB", time=2, style="super")
        self.game.effects.gi_off()
        self.delay(name='final_flash_delay', event_type=None, delay=1.5, handler=self.final_flash_uit)

    def final_flash_uit(self):
        for i in (self.yellow + self.blue + self.orange + self.green + self.red):
            self.game.effects.drive_lamp(i, 'off')
        self.game.effects.gi_on()

    def verticaal_aan1(self):
        for i in self.yellow:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan2(self):
        for i in self.blue:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan3(self):
        for i in self.orange:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan4(self):
        for i in self.green:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan5(self):
        for i in self.red:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_uit1(self):
        for i in self.yellow:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit2(self):
        for i in self.blue:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit3(self):
        for i in self.orange:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit4(self):
        for i in self.green:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit5(self):
        for i in self.red:
            self.game.effects.drive_lamp(i, 'off')

    def visor_check(self):
        if self.visor_count == 1:
            self.verticaal_aan1()

        elif self.visor_count == 2:
            self.verticaal_aan2()

        elif self.visor_count == 3:
            self.verticaal_aan3()

        elif self.visor_count == 4:
            self.verticaal_aan4()

        elif self.visor_count == 5:
            self.verticaal_aan5()

            # hierna uitbreiden voor horizontale lijnen.

    def sw_visor1_active(self, sw):
        if self.visor_count == 1:
            self.game.sound.play('sound_explosion_spaceship') 
            self.visor_count += 1
            self.verticaal_uit1()
            self.visor_check()
            return procgame.game.SwitchStop
        else:
            self.game.sound.play('sound_laser_gun_one_shot')

    def sw_visor2_active(self, sw):
        if self.visor_count == 2:
            self.game.sound.play('sound_explosion_spaceship')
            self.visor_count += 1
            self.verticaal_uit2()
            self.visor_check()
            return procgame.game.SwitchStop
        else:
            self.game.sound.play('sound_laser_gun_one_shot')

    def sw_visor3_active(self, sw):
        if self.visor_count == 3:
            self.game.sound.play('sound_explosion_spaceship')
            self.visor_count += 1
            self.verticaal_uit3()
            self.visor_check()
            return procgame.game.SwitchStop
        else:
            self.game.sound.play('sound_laser_gun_one_shot')

    def sw_visor4_active(self, sw):
        if self.visor_count == 4:
            self.game.sound.play('sound_explosion_spaceship')
            self.verticaal_uit4()
            self.visor_count += 1
            self.visor_check()
            return procgame.game.SwitchStop
        else:
            self.game.sound.play('sound_laser_gun_one_shot')

    def sw_visor5_active(self, sw):
        if self.visor_count == 5:
            self.game.sound.play('sound_explosion_spaceship')
            self.verticaal_uit5()
            self.final_flash()
            self.game.score(100000)
            self.game.current_player().set_mode_running(False)
        else:
            self.game.sound.play('sound_laser_gun_one_shot')

    def sw_outhole_active(self, sw):
            self.game.modes.remove(self)
            return procgame.game.SwitchStop
    def sw_outhole_active_for_3200ms(self, sw):
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
            return procgame.game.SwitchStop
