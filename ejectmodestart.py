# Control for main modes

from procgame import *
from mode_1 import *
from mode_2 import *
from mode_3 import *
from mode_4 import *
from mode_5 import *
from mode_6 import *
from mode_7 import *
import random

# Hoi ik ben er

# all necessary paths
game_path = "/home/pi/VXtra_start/"
dmd_path = game_path + "dmd/"
lampshow_path = game_path + "lampshows/"


class EjectModestart(game.Mode):
    def __init__(self, game, priority):
        super(EjectModestart, self).__init__(game, priority)
        self.planets = ['planet1', 'planet2', 'planet3', 'planet4', 'planet5',
                        'planet6', 'planet7', 'planet8', 'planet9']
        self.musicjes = ['music_backtothefuture', 'music_doctorwho', 'music_galaxysong', 'music_hitchhiker', 
                         'music_mario_invincible', 'music_interstellarcornfieldchase', 'music_starwars_theme', 
                         'music_imperialmarch', 'music_starwars_cantina_band']

    def mode_started(self):
        print "ejectmodestart started"
        self.Mode1_object = Mode1(self.game, 50)
        self.Mode2_object = Mode2(self.game, 51)
        self.Mode3_object = Mode3(self.game, 52)
        self.Mode4_object = Mode4(self.game, 53)
        self.Mode5_object = Mode5(self.game, 54)

        self.game.current_player().eject_mode_object = self

        # Dit zijn alleen referenties naar de arrays in current_player!
        self.modes = self.game.current_player().eject_mode_modes
        self.played_modes = self.game.current_player().eject_mode_played_modes

        if len(self.modes) == 0:
            self.modes.append(self.Mode1_object)
            self.modes.append(self.Mode2_object)
            self.modes.append(self.Mode3_object)
            self.modes.append(self.Mode4_object)
            self.modes.append(self.Mode5_object)

            del self.played_modes[:]

            print "Reset modes and played modes"
        self.mode_enabled = True
        self.random_next()
        # self.game.lampctrl.register_show('startmode', lampshow_path + "Planeten_short_flasher.lampshow")
        self.update_lamps()

    def sw_eject_active_for_500ms(self, sw):
        print "Eject-switch activated"
        if self.mode_enabled:
            if not self.game.current_player().mode_running:
                # Effects and score
                self.game.sound.fadeout_music(500)
                # self.game.lampctrl.play_show('startmode', repeat=False)
                self.game.sound.play("sound_evillaugh")
                self.game.score(2500)

                self.start_mode(self.next_mode)
                self.game.current_player().mode_running = True
            else:
                self.game.score(2500)
                self.game.effects.eject_ball('eject')
        self.update_lamps()

    def mode_running_changed(self, mode_running):
        print "mode running changed"
        if not mode_running:
            print "mode running changed --> mode done"
            # Mode has stopped running
            self.played_modes.append(self.next_mode)
            self.random_next()
            self.update_lamps()

    def stop_this_mode(self, mode_to_stop):
        if self.modes[self.next_mode] is mode_to_stop:
            try:
                self.game.modes.remove(mode_to_stop)
                self.game.current_player().mode_running = False
                self.played_modes.append(self.next_mode)
                self.random_next()
                music_track = random.choice(self.musicjes)
                self.game.sound.play_music(music_track, loops=-1)
                self.update_lamps()
            except ValueError:
                raise ValueError('mode_to_stop was not in the ModeQueue')
#        else:
#            raise ValueError('mode_to_stop was not the mode which was running')

    def random_next(self):
        print "Finding random next mode"
        # Ongespeelde modes zoeken
        unplayed_modes = []
        for i in range(0, len(self.modes)):
            if i not in self.played_modes:
                unplayed_modes.append(i)
        print "played modes:", self.played_modes
        print "unplayed modes:", unplayed_modes

        if len(unplayed_modes) == 0:
            # TODO all modes are played
            self.all_modes_played()
            return

        self.next_mode = random.choice(unplayed_modes)
        print "new next mode:", self.next_mode

    def all_modes_played(self):
        print "All modes played"
        self.game.score(100000)
        del self.game.current_player().eject_mode_played_modes[:]
        self.random_next()
        self.update_lamps()

    def sw_slingL_active(self, sw):
        self.sling_active()

    def sw_slingR_active(self, sw):
        self.sling_active()

    def sw_Ubumper_active(self, sw):
        self.sling_active()
    def sw_Lbumper_active(self, sw):
        self.sling_active()
    def sw_Bbumper_active(self, sw):
        self.sling_active()

    def sling_active(self):
        print "Sling activated"
        if not self.game.current_player().mode_running:
            # Alle planeetlampen uitzetten
            for planet in self.planets:
                self.game.effects.drive_lamp(planet, "off")

            self.random_next()

            if self.next_mode != -1:
                self.update_lamps()

    def sw_rampexit_active(self, sw):
        if self.game.current_player().mode_running == False and self.mode_enabled == False:
            self.mode_enabled = True
            self.game.sound.play("sound_2clash")
            self.update_lamps()

    def start_mode(self, mode):
        self.game.modes.add(self.modes[mode])
        print "ejectmodestart started a mode"

    def update_lamps(self):
        if self.game.current_player().mode_running:
            self.game.effects.drive_lamp('eject0', 'on')
        elif self.mode_enabled:
            self.game.effects.drive_lamp('eject0', 'medium')
            self.game.effects.drive_lamp('score_energy', 'on')
            self.game.effects.drive_lamp('solar_energy', 'on')
        else:
            self.game.effects.drive_lamp('eject0', 'off')
            self.game.effects.drive_lamp('score_energy', 'medium')
            self.game.effects.drive_lamp('solar_energy', 'medium')

        # First switch off all planets
        for planet in self.planets:
            self.game.effects.drive_lamp(planet, 'off')

        for mode_index in self.played_modes:
            self.game.effects.drive_lamp(self.planets[mode_index], 'on')

        if self.game.current_player().mode_running:
            # The self.next_mode mode is now running
            self.game.effects.drive_lamp(self.planets[self.next_mode], 'fast')
        else:
            # The self.next_mode mode will be the next to be played
            self.game.effects.drive_lamp(self.planets[self.next_mode], 'medium')
