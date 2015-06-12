# Visor

from procgame import *


# all paths
game_path = "/home/pi/VXtra_start/"
sound_path = game_path +"sound/fx/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Visor_up_down(game.Mode):

        def __init__(self, game, priority):
                super(Visor_up_down, self).__init__(game, priority)

        def mode_started(self):
                if self.game.current_player().visor_position=='up' and not self.visor_active():
                        self.visor_move()

        def mode_stopped(self):
                pass

        def visor_move(self):
                self.game.coils.Visormotor.enable()

        def visor_active(self):
                return self.game.switches.visorClosed.is_active()
                
## switches
                


