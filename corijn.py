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

class Corijn(game.Mode):
        def __init__(self, game, priority):
            super(Corijn, self).__init__(game, priority)

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
                if self.shotcount==1:
                        self.game.effects.drive_lamp('advance_planet','medium')
                if self.shotcount==2:
                        self.game.effects.drive_lamp('advance_planet','fast')
                if self.shotcount==3:
                        self.game.effects.drive_lamp('advance_planet','on')
		# ik heb er eentje bij gedaan (Corijn)
                if self.shotcount==4:
			self.game.effects.drive_lamp('advance_planet','on')


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
                        self.game.effects.flashers_flash(time=1)
		#hier heb ik er ook eentje bij gedaan (Corijn)
                elif self.shotcount==4:
			self.game.score(100000)
			self.game.sound.play("geluid3")
			self.game.effects.flashers_flash(time=2)
			self.shotcount=0
			self.super_mode()
                self.update_lamps()
        


## super mode
	# probeerseltje
        def super_mode(self):
		if self.shotcount==4:
			self.game.effects.drive_lamp('yellow1','on')
			self.game.effects.drive_lamp('yellow2','on')
			self.game.effects.drive_lamp('yellow3','on')
			self.game.effects.drive_lamp('yellow4','on')
			

## switches
        def sw_advanceplanet_active(self,sw):
                self.shotcount+=1
                self.check_progress()
