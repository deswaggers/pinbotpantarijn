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


class Mode3(game.Mode):
    def __init__(self, game, priority):
        super(Mode3, self).__init__(game, priority)

    def mode_started(self):
        self.score_layer = dmd.TextLayer(90, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)
        self.raise_layer = dmd.TextLayer(5, 2, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
        self.update_lamps()
        ## eerst instructies in beeld, daarna na delay pas bal eruit gooien en mode beginnen
        self.visor_count = 1
        self.visor_check()
        self.hit()

        self.yellow = ["yellow1", "yellow2", "yellow3", "yellow4", "yellow5"]
        self.blue = ["blue1", "blue2", "blue3", "blue4", "blue5"]
        self.orange = ["orange1", "orange2", "orange3", "orange4", "orange5"]
        self.green = ["green1", "green2", "green3", "green4", "green5"]
        self.red = ["red1", "red2", "red3", "red4", "red5"]

    def mode_stopped(self):
        self.game.sound.play_music('music_starwars_intro', loops=-1)
        self.game.current_player().mode_running = False
        self.layer = None

    ## niet nodig voor ons plan/project.
    ##        def drops_reset(self):
    ##                self.game.coils.Drops_RightInsBFlash.pulse(120)
    ##                self.dropscount=0
    ##                self.drop_timer = 0
    ##                self.game.effects.drive_lamp('drops','medium')

    def verticaal_aan1(self):
        for i in self.yellow:
            self.game.effects.drive_lamp(i, 'fast')

    def verticaal_aan2(self):
        for i in self.blue:
            self.game.effects.drive_lamp(i, 'fast')

    def verticaal_aan3(self):
        for i in self.orange:
            self.game.effects.drive_lamp(i, 'fast')

    def verticaal_aan4(self):
        for i in self.green:
            self.game.effects.drive_lamp(i, 'fast')

    def verticaal_aan5(self):
        for i in self.red:
            self.game.effects.drive_lamp(i, 'fast')

    def verticaal_uit1(self):
        for i in self.yellow:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit2(self):
        for i in self.blue:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit3(self):
        for i in self.orange:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit4(self):
        for i in self.green:
            self.game.effects.drive_lamp(i, 'off')

    def verticaal_uit5(self):
        for i in self.red:
            self.game.effects.drive_lamp(i, 'off')

    def visor_check(self):
        if self.visor_count == 1:
            self.verticaal_aan1()

        elif self.visor_count == 2:
            self.verticaal_aan2()

        elif self.visor_count == 3:
            self.verticaal_aan3()

        elif self.visor_count == 4:
            self.verticaal_aan4()

        elif self.visor_count == 5:
            self.verticaal_aan5()
            self.visor_count = 1
            # hierna uitbreiden voor horizontale lijnen.

    def hit(self):
        if self.visor_count == 1 and self.game.switches.visor1.is_active():
            self.visor_count += 1
            self.verticaal_uit1()
            self.visor_check()
        elif self.visor_count == 2 and self.game.switches.visor2.is_active():
            self.visor_count += 1
            self.verticaal_uit2()
            self.visor_check()
        elif self.visor_count == 3 and self.game.switches.visor3.is_active():
            self.visor_count += 1
            self.verticaal_uit3()
            self.visor_check()
        elif self.visor_count == 4 and self.game.switches.visor4.is_active():
            self.visor_count += 1
            self.verticaal_uit4()
            self.visor_check()
        elif self.visor_count == 5 and self.game.switches.visor5.is_active():
            self.verticaal_uit5()




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
                self.game.effects.drive_lamp('droptop', 'on')
            elif self.drop_timer >= 4:
                self.game.effects.drive_lamp('droptop', 'fast')
            elif self.drop_timer >= 2:
                self.game.effects.drive_lamp('droptop', 'medium')
            else:
                self.game.effects.drive_lamp('droptop', 'slow')

            if self.game.switches.droptarget2.is_active():
                self.game.effects.drive_lamp('dropmid', 'on')
            elif self.drop_timer >= 4:
                self.game.effects.drive_lamp('dropmid', 'fast')
            elif self.drop_timer >= 2:
                self.game.effects.drive_lamp('dropmid', 'medium')
            else:
                self.game.effects.drive_lamp('dropmid', 'slow')

            if self.game.switches.droptarget3.is_active():
                self.game.effects.drive_lamp('dropbottom', 'on')
            elif self.drop_timer >= 4:
                self.game.effects.drive_lamp('dropbottom', 'fast')
            elif self.drop_timer >= 2:
                self.game.effects.drive_lamp('dropbottom', 'medium')
            else:
                self.game.effects.drive_lamp('dropbottom', 'slow')
        else:
            self.game.effects.drive_lamp('drops', 'slow')



        ## switches

    def sw_droptarget1_active_for_200ms(self, sw):
        self.drops_check()

    def sw_droptarget2_active_for_200ms(self, sw):
        self.drops_check()

    def sw_droptarget3_active_for_200ms(self, sw):
        self.drops_check()
