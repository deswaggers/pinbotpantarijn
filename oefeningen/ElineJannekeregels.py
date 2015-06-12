import procgame
from procgame import *
import locale

# all paths
game_path = "C:\P-ROC\pyprocgame-master\games\VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Ej_regels(game.Mode):
        def __init__(self, game, priority):
            super(Ej_regels, self).__init__(game, priority)

        def mode_started(self):
            print("Deze regels zijn gestart, mijn regels heten: ......(op dit moment 'Regels1, maar die gaan we hernoemen")
            self.shotcount=0
            self.check_progress()
            # deze variabele wordt het begin van elke bal op 0 gezet. Stel dat je een variabele wilt die
            # per speler wordt onthouden, gebruik dan: self.game.current_player().shotcount=0. Bij de 'if' moet dit dan ook weer.
            

        def mode_stopped(self):
            print("Debug, regels ..... zijn weer gestopt")

## Lamps

        def update_lamps(self):
                if self.shotcount==0:
                        self.game.effects.drive_lamp('advance_planet','slow')
                if self.shotcount==1:
                        self.game.effects.drive_lamp('advance_planet','medium')
                if self.shotcount==2:
                        self.game.effects.drive_lamp('advance_planet','fast')
                if self.shotcount==3:
                        self.game.effects.drive_lamp('advance_planet','on')
                if self.shotcount==6:
                        self.game.effects.drive_lamp('planet1', 'slow')
                if self.shotcount==7:
                        self.game.effects.drive_lamp('planet1', 'medium')
                if self.shotcount==8:
                        self.game.effects.drive_lamp('planet1', 'chaos')


## mode functions

        def check_progress(self):
                if self.shotcount==1:
                        self.game.score(5000)
                        # neem hier de naam van het bestand, bv. 'geluid1.wav' wordt 'geluid1'
                        self.game.sound.play("geluid_1")
                        self.game.effects.lower_flashers_flash()
                elif self.shotcount==2:
                        self.game.score(10000)
                        self.game.sound.play("geluid2")
                        self.game.effects.lower_flashers_flash()
                elif self.shotcount==3:
                        self.game.score(50000)
                        self.game.sound.play("geluid3")
                        self.game.effects.flashers_flash(time=2)
                        self.shotcount=0
                self.update_lamps()
        
## switches
        def sw_advanceplanet_active(self,sw):
                self.shotcount+=1
                self.check_progress()

        def sw_droptarget1_active(self,sw):
                self.shotcount+=1
                self.check_progress()
                self.game.effects.drive_lamp('droptop', 'on')
        def sw_droptarget2_active(self,sw):
                self.shotcount+=1
                self.check_progress()
                self.game.effects.drive_lamp('droptop', 'on')
        def sw_droptarget3_active(self,sw):
                self.shotcount+=1
                self.check_progress()
                self.game.effects.drive_lamp('droptop', 'on')



                
