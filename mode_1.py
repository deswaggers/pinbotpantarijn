# Mode bumpers
import procgame
from procgame import *
import random


# All paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Mode1(game.Mode):

        def __init__(self, game, priority):
                super(Mode1, self).__init__(game, priority)

        def mode_started(self):

                # Hieronder worden 3 'lagen' gemaakt die later gebruikt worden voor op het scherm.
                # De lagen zijn nog niet gevuld, maar er wordt hier alleen gebruik gemaakt van text, en de plaats op het scherm van 128 bij 32 pixels wordt alvast bepaald,
                # evenals de uitlijning (1 x gecentreerd en 2 keer links)

                self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.raise_layer = dmd.TextLayer(8, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.text_layer = dmd.TextLayer(8, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)

                # update_lamps functie wordt aangeroepen om lampjes aan te zetten.

                self.update_lamps()

                # eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen. Delay is in seconden
                # na 2 seconden
                self.delay(name='Mode_start_na_eject', event_type=None, delay=2, handler=self.mode_start_na_eject)

        def mode_start_na_eject(self):
                # De bal wordt uit het gat gegooid waar de mode is 'gestart' (linksboven)
                self.game.effects.eject_ball('eject')

                # Muziek aan (er kan maar 1 muziekje tegelijk, geluiden afspelen kan wel met meerdere door elkaar.
                # music_harp.wav zit in de map 'muziek' en wordt vanzelf ook herkend
                self.game.sound.play_music('music_harp', loops=-1)

                # variabelen worden aangemaakt
                self.bumperscore=40  # dit wordt straks gebruikt bij elke keer dat een bumper wordt geraakt
                self.bumperraise=0   # kijk later verderop in de code wat deze 3 doen
                self.time_left=19
                self.shoot_message=True
                self.totalscore=0    # voor aan het einde van de mode: een variabele die bijhoudt hoeveel er totaal wordt gescoord

                ## self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown) # over 1 seconde wordt de functie 'countdown' uitgevoerd
                ## self.bumpers_hit()   # Deze 2 stonden er, maar mogen weg volgens mij... nog niet kunnen testen.

                self.countdown() # Voer de functie countdown meteen uit (zie verderop)

        def mode_stopped(self):
                # voor het 'doorschieten' van de bal
                self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

                # Dit zorgt ervoor dat het scherm weer 'leeg' is en terug gaat naar de basis-score
                self.layer = None

# Switches
        # de komende 5 zorgen allemaal dat bumpers_hit wordt uitgevoerd en dat de rest van het spel niet ook beinvloed
        # wordt door het raken van de switch (niet dat je score uit deze mode krijgt EN ook nog van het gewone spel
        def sw_Ubumper_active(self,sw):
                self.bumpers_hit()
                return procgame.game.SwitchStop
        def sw_Bbumper_active(self,sw):
                self.bumpers_hit()
                return procgame.game.SwitchStop
        def sw_Lbumper_active(self,sw):
                self.bumpers_hit()
                return procgame.game.SwitchStop
        def sw_slingR_active(self,sw):
                self.bumpers_hit()
                return procgame.game.SwitchStop
        def sw_slingL_active(self,sw):
                self.bumpers_hit()
                return procgame.game.SwitchStop

        # Als de ramp wordt geraakt, krijg je wat extra tijd, met 23 seconden als maximum
        def sw_rampexit_active(self, sw):
                self.time_left+=5
                if self.time_left>23:
                        self.time_left=23
                self.text_layer.set_text("EXTRA 5 SECONDS, " +str(self.time_left)+ "LEFT",True)
                self.layer = dmd.GroupedLayer(128, 32, [self.text_layer])
                self.game.sound.play("sound_hand-clap-echo")

# Als de bal draint tijdens de mode:
        def sw_outhole_active(self, sw):
                self.displaytotalscore()
                return procgame.game.SwitchStop


# Lampen
        def update_lamps(self):
                # lampjes bij de ramp worden aangezet, omdat je daar extra tijd kan halen.
                self.game.effects.drive_lamp('score_energy','fast')
                self.game.effects.drive_lamp('solar_energy','medium')
                # Wat nog leuk zou zijn, is een 'tijdbalk' voor hoeveel tijd je nog hebt bij elke getimede mode:
                # planeten van allemaal aan (bovenste knipperen) tot pluto, dan voorbij als pluto uit gaat? Bij
                # sluiten mode moet dan de 'oude staat' van het gewone spel hersteld worden.



# Mode functions

        def energyflash(self):
                # Als deze functie wordt uitgevoerd, wordt de 'flasher' onder de pop-bumpers even aan gezet
                self.game.coils.Solenoidselect.pulse(90)
                self.game.coils.RampLow_EnergyFlash.pulse(70)

        def countdown(self): # Door de laatste regel in deze functie, wordt 'countdown' elke seconde uitgevoerd

                # Elke keer 1 eraf, en countdown gaat elke seconde, dus timer wordt 1 minder per seconde
                self.time_left-=1

                # De variabele shoot_message begint op True, gaat dan naar False, dan weer naar True, etc...
                self.shoot_message =  not self.shoot_message

                # Roep de functie shoot_bumpers_animation aan. Dit doet ie dus elke seconde
                self.shoot_bumpers_animation()

                # als de timer op 0 staat, voert ie de functie 'displaytotalscore' uit
                if self.time_left<1:
                        self.displaytotalscore()
                # elke seconde wordt countdown weer gestart
                self.delay(name='Mode_countdown', event_type=None, delay=1, handler=self.countdown)



        def displaytotalscore(self):  # deze voerde hij uit, als de tijd op 0 stond, weet je nog? Zie een paar regels hier boven

                # Vul de eerder gemaakte 'text_layer' met de tekst 'TOTAL SCORE' (dit lettertype kan alleen
                # hoofdletters), gevolgd door hoeveel er totaal in de variabele 'totalscore' zit.
                self.text_layer.set_text('TOTAL SCORE '+str(self.totalscore),True)

                # Maak een animatie-laag aan, waarin een gif wordt geladen. Voor nu een 'placeholder'-plaatje
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_2.gif') #Als het goed is kan ie ook rechtstreeks png-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=4)

                # zorg ervoor dat het 'zwart' in het plaatje doorzichtig wordt
                self.animation_layer.composite_op = "blacksrc"
                # self.layer laat het spel standaard zien. Nu maken we self.layer een 'groepslaag': een combinatie van
                # 1 plaatje (de animation_layer) en een tekstlaag
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.text_layer])

                # Na 1,4 seconden de score laten zien, voert ie 'endmode' uit
                self.delay(name='End_mode', event_type=None, delay=1.4, handler=self.endmode)
                # Muziek fade-out. 1200 miliseconde, dus geluid is uit voordat 'endmode' wordt uitgevoerd.
                self.game.sound.fadeout_music(1200)
                # Oh ja, de lampjes die eerder waren aangezet, moeten wel uit
                self.game.effects.drive_lamp('score_energy','off')
                self.game.effects.drive_lamp('solar_energy','off')
        def endmode(self):
                self.game.current_player().stop_eject_mode_mode(self) # De mode wordt 'verwijderd' / gestopt

        def bumpers_hit(self):  # Deze wordt elke keer uitgevoerd als een bumper of een slingshot wordt geraakt
                # Score-systeem:
                # bumperraise zort voor per '7 hits' dat de bumperscore omhoog gaat
                self.bumperraise+=1
                if self.bumperraise>6:
                        self.bumperscore+=20
                        self.bumperraise=0
                # per keer wordt de bumperscore-waarde bij de score geteld, en ook bij de variabele totalscore
                self.game.score(self.bumperscore)
                self.totalscore+=self.bumperscore

                # Sound: verschillende geluiden bij verschillende waardes van de variabele bumperscore
                if self.bumperscore<=60:
                        self.game.sound.play("sound_lasergun1")
                elif self.bumperscore<=100:
                        self.game.sound.play("sound_lasergun2")
                else:
                        self.game.sound.play("sound_lasergun3")

                # Display: weer verschillende lagen, paar met tekst, waarvan 1 met willekeurig 3 uitroepen en
                # een 'balkje'. Dat balkje moet nog meegaan met de tijd
                # Let op: deze zitten in de functie 'bumper_hit', dus onderstaande wordt ook steeds uitgevoerd met
                # het raken van een popbumper of slingshot
                self.score_layer.set_text("EACH  " +str(self.bumperscore),True)
                self.raise_layer.set_text("RAISE AT 6  " +str(self.bumperraise),True)
                x=random.random()
                if x>0.7:
                        self.text_layer.set_text('BAM!',True)
                elif x>0.4:
                        self.text_layer.set_text('WHAM',True)
                else:
                        self.text_layer.set_text('BOOM',True)
                anim = dmd.Animation().load(dmd_path+'DMD_Mode1_1.gif') #Als het goed is kan ie ook rechtstreeks gif-bestanden aan
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                self.animation_layer.composite_op = "blacksrc"
                ##### deze niet nodig volgens mij: nog niet gecheckt #######
                # anim = dmd.Animation().load(dmd_path+'life_bar.dmd')
                # self.lifebar_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=0)
                # self.lifebar_layer.composite_op = "blacksrc"
                ############################################################
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.lifebar_layer,self.score_layer, self.raise_layer, self.text_layer])

        def shoot_bumpers_animation(self):
                # Deze werd elke seconde aangeroepen. Als er dus geen slingshot of bumper
                # wordt geraakt, dan is dit steeds in beeld
                if self.shoot_message==True:
                        self.text_layer.set_text('SHOOT THE BUMPERS',True)
                else:
                        self.text_layer.set_text('SHOOT THE RAMP',True)
                self.score_layer.set_text("EACH:: " +str(self.bumperscore),True)
                self.raise_layer.set_text("RAISE AT 6: . " +str(self.bumperraise),True) ## modetimer met healthbar/tijdbalk doen?
                anim = dmd.Animation().load(dmd_path+'life_bar.dmd') # Een dmd bestand bestaat uit frames van plaatjes die zijn omgezet in iets leesbaars voor PROCGAME

                ##########
                ##self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                #############Deze zinnen hieronder nog testen: 2 mogelijkheden
                #####self.animation_layer = dmd.AnimatedLayer(frames=anim.frames[25-self.time_left], opaque=False, repeat=False, hold=True, frame_time=0)
                #############

                self.lifebar_layer = dmd.FrameLayer(opaque=True, frame = anim.frames[24-self.time_left])
                self.lifebar_layer.composite_op = "blacksrc"
                self.layer = dmd.GroupedLayer(128, 32, [self.lifebar_layer, self.score_layer, self.raise_layer, self.text_layer])
