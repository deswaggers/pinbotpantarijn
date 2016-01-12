# Mode bumpers
import procgame
from procgame import *
import locale
import random


# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Mode3(game.Mode):

        def __init__(self, game, priority):
                super(Mode3, self).__init__(game, priority)
                

        def mode_started(self):
                self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
                self.raise_layer = dmd.TextLayer(5, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.update_lamps()
                ## eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
                self.delay(name='Mode_start_na_eject', event_type=None, delay=2, handler=self.mode_start_na_eject)
                visor_count = 1
                visor_check()
                hit()
                
                self.yellow = ["yellow1", "yellow2", "yellow3", "yellow4", "yellow5"]
                self.blue=["blue1", "blue2", "blue3", "blue4", "blue5"]
                self.orange=["orange1", "orange2", "orange3", "orange4", "orange5"]
                self.green=["green1", "green2", "green3", "green4", "green5"]
                self.red=["red1", "red2", "red3", "red4", "red5"]

        def mode_stopped(self):
                self.game.sound.play_music('music_starwars_intro', loops=-1)
                self.game.current_player().mode_running=False
                self.layer = None

## niet nodig voor ons plan/project.
##        def drops_reset(self):
##                self.game.coils.Drops_RightInsBFlash.pulse(120)
##                self.dropscount=0
##                self.drop_timer = 0
##                self.game.effects.drive_lamp('drops','medium')

        def 1_verticaal_aan(self):
                for i in self.yellow:
                        self.game.effects.drive_lamp(i,'fast')

         def 2_verticaal_aan(self):
                for i in self.blue:
                        self.game.effects.drive_lamp(i,'fast')

         def 3_verticaal_aan(self):
                for i in self.orange:
                        self.game.effects.drive_lamp(i,'fast')

         def 4_verticaal_aan(self):
                for i in self.green:
                        self.game.effects.drive_lamp(i,'fast')

         def 5_verticaal_aan(self):
                for i in self.red:
                        self.game.effects.drive_lamp(i,'fast')

         def 1_verticaal_uit(self):
                for i in self.yellow:
                        self.game.effects.drive_lamp(i,'off')

        def 2_verticaal_uit(self):
                for i in self.blue:
                        self.game.effects.drive_lamp(i,'off')

        def 3_verticaal_uit(self):
                for i in self.orange:
                        self.game.effects.drive_lamp(i,'off')

        def 4_verticaal_uit(self):
                for i in self.green:
                        self.game.effects.drive_lamp(i,'off')

        def 5_verticaal_uit(self):
                for i in self.red:
                        self.game.effects.drive_lamp(i,'off')





        def visor_check(self):
                if visor_count == 1:
                        1_verticaal_aan()
                       
                elif visor_count == 2:
                        2_verticaal_aan()
                        
                elif visor_count == 3:
                        3_verticaal_aan()
                        
                elif visor_count == 4:
                        4_verticaal_aan()
                        
                elif visor_count == 5:
                        5_verticaal_aan()
                        visor_count = 1
                # hierna uitbreiden voor horizontale lijnen.

        def hit(self):
                if visor_count == 1 and self.game.switches.visor1.is_active():
                        visor_count += 1
                        1_verticaal_uit()
                        visor_check()
                elif visor_count == 2 and self.game.switches.visor2.is_active():
                        visor_count += 1
                        2_verticaal_uit()
                        visor_check()
                elif visor_count == 3 and self.game.switches.visor3.is_active():
                        visor_count += 1
                        3_verticaal_uit()
                        visor_check()
                elif visor_count == 4 and self.game.switches.visor4.is_active():
                        visor_count += 1
                        4_verticaal_uit()
                        visor_check()
                elif visor_count == 5 and self.game.switches.visor5.is_active():
                        5_verticaal_uit()
                        
                        


##        def drops_check(self):
##                if self.dropscount==0:
##                        self.dropscount=1
##                        self.game.score(200)
##                        #self.cancel_delayed('drop_timer')
##                        print "eerste droptarget"
##                        self.delay(name='drop_timer', event_type=None, delay=6, handler=self.drops_reset)
##                        
##                        
##                elif self.dropscount==1:
##                        self.dropscount=2
##                        self.game.score(1000)
##                        #self.cancel_delayed('drop_timer')
##                        self.delay(name='drop_timer', event_type=None, delay=6, handler=self.drops_reset)
##                        print "2e droptarget"
##
##                elif self.dropscount==2:
##                        self.game.score(10000)
##                        print "3e droptarget"
##                        self.cancel_delayed('drop_timer')
##                        self.drops_reset()
##                self.game.sound.play("sound_lasergun1")
##                self.update_lamps()

        def update_lamps(self):
                if self.game.switches.droptarget1.is_active() or self.game.switches.droptarget2.is_active() or self.game.switches.droptarget3.is_active():
                        if self.game.switches.droptarget1.is_active():
                                self.game.effects.drive_lamp('droptop','on')
                        elif self.drop_timer >= 4:
                                self.game.effects.drive_lamp('droptop','fast')
                        elif self.drop_timer >= 2:
                                self.game.effects.drive_lamp('droptop','medium')
                        else:
                                self.game.effects.drive_lamp('droptop','slow')

                        if self.game.switches.droptarget2.is_active():
                                self.game.effects.drive_lamp('dropmid','on')
                        elif self.drop_timer >= 4:
                                self.game.effects.drive_lamp('dropmid','fast')
                        elif self.drop_timer >= 2:
                                self.game.effects.drive_lamp('dropmid','medium')
                        else:
                                self.game.effects.drive_lamp('dropmid','slow')

                        if self.game.switches.droptarget3.is_active():
                                self.game.effects.drive_lamp('dropbottom','on')
                        elif self.drop_timer >= 4:
                                self.game.effects.drive_lamp('dropbottom','fast')
                        elif self.drop_timer >= 2:
                                self.game.effects.drive_lamp('dropbottom','medium')
                        else:
                                self.game.effects.drive_lamp('dropbottom','slow')
                else:
                        self.game.effects.drive_lamp('drops','slow')
            
                        
                
## switches
                
        def sw_droptarget1_active_for_200ms(self,sw):
                self.drops_check()

        def sw_droptarget2_active_for_200ms(self,sw):
                self.drops_check()

        def sw_droptarget3_active_for_200ms(self,sw):
                self.drops_check()
        
