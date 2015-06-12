import procgame
from procgame import *
import locale

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Tein(game.Mode):
        def __init__(self, game, priority):
            super(Tein, self).__init__(game, priority)

        def mode_started(self):
            print("Hello, Galaxy!")
    

        def mode_stopped(self):
            print("See ya later alligator")

        def sw_Loutlane_active(self, sw):
            self.game.effects.drive_lamp('planet1', 'fast')
            self.game.effects.drive_lamp('planet2', 'fast')
            self.game.effects.drive_lamp('planet3', 'fast')
            self.game.effects.drive_lamp('planet4', 'fast')
            self.game.effects.drive_lamp('planet5', 'fast')
            self.game.effects.flashers_flash()

        def sw_Routlane_active(self, sw):
            print("That was very bad of you")
            self.game.effects.drive_lamp('planet6', 'fast')
            self.game.effects.drive_lamp('planet7', 'fast')
            self.game.effects.drive_lamp('planet8', 'fast')
            self.game.effects.drive_lamp('planet9', 'fast')
            self.game.effects.drive_lamp('advance_planet', 'fast')
            self.game.effects.flashers_flash()

        def sw_Linlane_active(self, sw):
            self.game.effects.drive_lamp('planet1', 'fast')
            self.game.effects.drive_lamp('planet2', 'fast')
            self.game.effects.drive_lamp('planet3', 'fast')
            self.game.effects.drive_lamp('planet4', 'fast')
            self.game.effects.drive_lamp('planet5', 'fast')

        def sw_Rinlane_active(self, sw):
            self.game.effects.drive_lamp('planet6', 'fast')
            self.game.effects.drive_lamp('planet7', 'fast')
            self.game.effects.drive_lamp('planet8', 'fast')
            self.game.effects.drive_lamp('planet9', 'fast')
            self.game.effects.drive_lamp('advance_planet', 'fast')

##        def sw_advanceplanet_active(self, sw): 
##            self.game.effects.flahsers_flash()
