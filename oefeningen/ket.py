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

class Ket(game.Mode):
        def __init__(self, game, priority):
            super(Ket, self).__init__(game, priority)

        def mode_started(self):
            print("Deze regels zijn gestart, mijn regels heten: ......(op dit moment 'Regels1, maar die gaan we hernoemen")
            
            # deze variabele wordt het begin van elke bal op 0 gezet. Stel dat je een variabele wilt die
            # per speler wordt onthouden, gebruik dan: self.game.current_player().shotcount=0. Bij de 'if' moet dit dan ook weer.
            self.shotcount=0
            self.check_progress()

        def mode_stopped(self):
            print("Debug, regels ..... zijn weer gestopt")

## Lamps

        def update_lamps(self):
                if self.shotcount==0:
                        self.game.effects.drive_lamp('advance_planet','slow')
                        ##uiterst experimenteel regeltje, want lamptijd is negatief (en blijkbaar is de tijd altijd 2)
                        self.game.effects.drive_lamp('red1','superfast',-1)
                        self.game.effects.drive_lamp('red2','medium',6.9)
                        self.game.effects.drive_lamp('red3','slow',6.66)
                        self.game.effects.drive_lamp('red4','fast',4.20)
                        self.game.effects.drive_lamp('red5','slow',3.14)
                if self.shotcount==1:
                        self.game.effects.drive_lamp('orange1','medium')
                if self.shotcount==2:
                        self.game.effects.drive_lamp('orange1','fast')
                if self.shotcount==3:
                        self.game.effects.drive_lamp('orange1','on')


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
        def sw_10point1_active(self,sw):
                self.shotcount+=1
                self.check_progress()

##Als de flipperkast getilt wordt, dan knipperen lampjes.
        def sw_tilt_active(self,sw):
                self.game.effects.gi_blinking()

 
                

