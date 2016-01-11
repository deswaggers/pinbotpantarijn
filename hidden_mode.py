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


class HiddenMode(game.Mode):
        # Eerst een van vijf ronde switches rechts, dan een droptarget,
        # dan weer een van vijf, dan weer een droptarget -- in volgorde, achter elkaar

        def __init__(self, game, priority):
                super(HiddenMode, self).__init__(game, priority)
                self.bankHit1 = False
                self.dropHit1 = False
                self.bankHit2 = False
                self.dropHit2 = False

        def sw_Rbank1_active(self, sw):
                self.bank_hit()

        def sw_Rbank2_active(self, sw):
                self.bank_hit()

        def sw_Rbank3_active(self, sw):
                self.bank_hit()

        def sw_Rbank4_active(self, sw):
                self.bank_hit()

        def sw_Rbank5_active(self, sw):
                self.bank_hit()

        def sw_droptarget1_active(self, sw):
                self.drop_hit()

        def sw_droptarget2_active(self, sw):
                self.drop_hit()

        def sw_droptarget3_active(self, sw):
                self.drop_hit()

        def bank_hit(self):
                if not self.game.current_player().mode_running:


                if self.dropHit1:
                        self.bankHit2 = True
                else:
                        self.delay(name='Mode_activation_timer', event_type=None, delay=20, handler=self.time_out())

        def drop_hit(self):
                if self.bankHit2:
                        self.dropHit2 = True
                        if not self.game.current_player().mode_running:
                                self.start_mode()
                elif self.bankHit1:
                        self.dropHit1 = True

        def time_out(self):
                self.bankHit1 = self.dropHit1 = self.bankHit2 = self.dropHit2 = False

        def start_mode(self):
                self.delay(name='Mode_time')
                self.game.score(3000)

                # TODO
                pass

        def mode_started(self):
                self.knipper_lampen()

                self.text_layer = dmd.TextLayer(1, 1, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.text_layer.set_text("YOU HAVE UNLOCKED A HIDDEN MODE")
                self.layer = self.text_layer

        def knipper_lampen(self):
                self.game.effects.drive_lamp("planet1", "fast")
                self.game.effects.drive_lamp("planet2", "fast")
                self.game.effects.drive_lamp("planet3", "fast")
                self.game.effects.drive_lamp("planet4", "fast")
                self.game.effects.drive_lamp("planet5", "fast")
                self.game.effects.drive_lamp("planet6", "fast")
                self.game.effects.drive_lamp("planet7", "fast")
                self.game.effects.drive_lamp("planet8", "fast")
                self.game.effects.drive_lamp("planet9", "fast")

        def mode_stopped(self):
                self.game.sound.play_music('music_starwars_intro', loops=-1)
                self.game.current_player().mode_running = False
                self.layer = None
