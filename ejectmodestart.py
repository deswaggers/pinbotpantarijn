# Control for main modes

from procgame import *
from mode_1 import *
from mode_2 import *
from mode_3 import *

# all necessary paths
game_path = "/home/pi/VXtra_start/"
dmd_path = game_path + "dmd/"
lampshow_path = game_path + "lampshows/"


class EjectModestart(game.Mode):
    def __init__(self, game, priority):
        super(EjectModestart, self).__init__(game, priority)
        self.planets = ['planet1', 'planet2', 'planet3', 'planet4', 'planet5',
                        'planet6', 'planet7', 'planet8', 'planet9']

    def mode_started(self):
        self.Mode1_object = Mode1(self.game, 50)
        self.Mode2_object = Mode2(self.game, 51)
        self.Mode3_object = Mode3(self.game, 52)

        self.game.current_player().eject_mode_object = self

        self.modes = [self.Mode1_object, self.Mode2_object, self.Mode3_object]
        self.played_modes = []
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
                self.game.current_player().set_mode_running(True)
                self.mode_enabled = False
                self.update_lamps()
            else:
                self.game.score(2500)
        self.update_lamps()

    def mode_running_changed(self, mode_running):
        print "mode running changed"
        if not mode_running:
            # Mode has stopped running
            self.played_modes.append(self.next_mode)
            self.random_next()
            self.update_lamps()

    def random_next(self):
        # Ongespeelde modes zoeken
        unplayed_modes = []
        for i in range(0, len(self.modes)):
            if i not in self.played_modes:
                unplayed_modes.append(i)
        print "played modes:", self.played_modes
        print "unplayed modes:", unplayed_modes

        # Als alle modes al gespeeld zijn
        if len(unplayed_modes) == 0:
            self.next_mode = -1  # TODO

        self.next_mode = random.choice(unplayed_modes)
        print "new next mode:", self.next_mode

    def sw_slingL_active(self, sw):
        if not self.game.current_player().mode_running:
            # Alle planeetlampen uitzetten
            for planet in self.planets:
                self.game.effects.drive_lamp(planet, "off")

            self.random_next()
            self.update_lamps()

    def sw_rampexit_active(self, sw):
        if self.game.current_player().mode_running == False and self.mode_enabled == False:
            self.mode_enabled = True
            self.game.sound.play("sound_2clash")
            self.update_lamps()

    def start_mode(self, mode):
        self.game.modes.add(self.modes[mode])
        print "mode started"

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

        for mode_index in self.played_modes:
            self.game.effects.drive_lamp(self.planets[mode_index], 'on')

        if self.game.current_player().mode_running:
            self.game.effects.drive_lamp(self.planets[self.next_mode], 'fast')
        else:
            self.game.effects.drive_lamp(self.planets[self.next_mode], 'medium')
