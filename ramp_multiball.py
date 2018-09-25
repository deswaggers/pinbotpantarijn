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
lampshow_path = game_path +"lampshows/"


class RampMultiball(game.Mode):
    def __init__(self, game, priority):
        super(RampMultiball, self).__init__(game, priority)

    def mode_started(self):
        print "RampMultiball uit ramp_multiball.py is gestart"
        self.health=0
        self.instruction_layer = dmd.TextLayer(20, 20, self.game.fonts['num_09Bx7'], opaque=False)
        #self.game.lampctrl.register_show('multiball_start', lampshow_path +"planeten_short.lampshow")
        #self.game.lampctrl.register_show('visor_lampshow', lampshow_path +"Pinbot_1.lampshow")
        self.delay(name='start_rampMB', event_type=None, delay=5, handler=self.start_rampMB)
        self.display_instructions()
        self.twoballsinplay = False
        self.game.lampctrl.stop_show()
        self.all_lamps_off()
        self.startLampSituation()
        self.game.current_player().mode_running = True

    def all_lamps_off(self):
        for x in range(1,6):
            self.game.effects.drive_lamp('yellow'+str(x),'off')
            self.game.effects.drive_lamp('green'+str(x),'off')
            self.game.effects.drive_lamp('orange'+str(x),'off')
            self.game.effects.drive_lamp('blue'+str(x),'off')
            self.game.effects.drive_lamp('red'+str(x),'off')
        self.visor1 = 0
        self.visor2 = 0
        self.visor3 = 0
        self.visor4 = 0
        self.visor5 = 0


    def startLampSituation(self):
        ## SAMEN OP EINDE GEDAAN, VERDER UTIWERKEN
        self.game.effects.drive_lamp('yellow1','fast')
        self.game.effects.drive_lamp('green1','fast')
        self.game.effects.drive_lamp('orange1','fast')
        self.game.effects.drive_lamp('blue1','fast')
        self.game.effects.drive_lamp('red1','fast')
        self.game.effects.gi_off()



    def start_rampMB(self):
        print "nu is start_rampMB gestart, dus moet ie een bal geven"
        self.game.trough.launch_balls(1)
        self.game.sound.play_music('music_harp', loops=-1)


    def mode_tick(self):
        if ((self.game.trough.num_balls_in_play<2) and self.twoballsinplay):
            self.stop_rampmultiball()


    def stop_rampmultiball(self):
        self.game.sound.play_music('music_2017_creepy_alien_music')
        self.game.effects.ramp_down()
        self.game.current_player().mode_running = False
        self.game.modes.remove(self)
        self.all_lamps_off(self)
        self.layer = None

    def mode_stopped(self):
        self.layer = None
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)

    def display_instructions(self):
        anim = dmd.Animation().load(dmd_path+'life_bar.dmd') # Een dmd bestand bestaat uit frames van plaatjes die zijn omgezet in iets leesbaars voor PROCGAME
        self.hit_layer = dmd.FrameLayer(opaque=True, frame = anim.frames[24-self.health])
        self.hit_layer.composite_op = "blacksrc"
        self.instruction_layer.set_text('RAMP MULTIBALL GESTART')
        self.layer=dmd.GroupedLayer(128,32,[self.hit_layer, self.instruction_layer])


    def update_lamps_1(self):
        for z in range(1,self.visor1+1):
            self.game.effects.drive_lamp('yellow'+str(z),'on')
        if self.visor1 <5:
            self.knipperendevisor1 = self.visor1 +1
            self.game.effects.drive_lamp('yellow'+str(self.knipperendevisor1),'fast')


    def update_lamps_2(self):
        for y in range(1,self.visor2+1):
            self.game.effects.drive_lamp('blue'+str(y),'on')
        if self.visor2 <5:
            self.knipperendevisor2 = self.visor2 +1
            self.game.effects.drive_lamp('blue'+str(self.knipperendevisor2),'fast')


    def update_lamps_3(self):
        for a in range(1,self.visor3+1):
            self.game.effects.drive_lamp('orange'+str(a),'on')
        if self.visor3 <5:
            self.knipperendevisor3 = self.visor3 +1
            self.game.effects.drive_lamp('orange'+str(self.knipperendevisor3),'fast')


    def update_lamps_4(self):
        for b in range(1,self.visor4+1):
            self.game.effects.drive_lamp('green'+str(b),'on')
        if self.visor4 <5:
            self.knipperendevisor4 = self.visor4 +1
            self.game.effects.drive_lamp('green'+str(self.knipperendevisor4),'fast')


    def update_lamps_5(self):
        for c in range(1,self.visor5+1):
            self.game.effects.drive_lamp('red'+str(c),'on')
        if self.visor5 <5:
            self.knipperendevisor5 = self.visor5 +1
            self.game.effects.drive_lamp('red'+str(self.knipperendevisor5),'fast')


    def row_points(self, rows):
        if self.visor1>=rows and self.visor2>=rows and self.visor3>=rows and self.visor4>=rows and self.visor5>=rows:
            self.game.score(10**rows)


##Hieronder alle Switches
    def sw_scoreEnergy_active(self,sw):
        self.health+=1
        self.display_instructions()
        self.game.effects.drive_lamp('eject3','fast')
        return procgame.game.SwitchStop


    def sw_visor1_active(self,sw):
        if self.visor1<5:
            self.visor1+=1
            self.update_lamps_1()
        self.game.score(150*self.visor1)
        return procgame.game.SwitchStop

    def sw_visor2_active(self,sw):
        if self.visor2<5:
            self.visor2+=1
            self.update_lamps_2()
        self.game.score(150*self.visor2)
        return procgame.game.SwitchStop

    def sw_visor3_active(self,sw):
        if self.visor3<5:
            self.visor3+=1
            self.update_lamps_3()
        self.game.score(150*self.visor3)
        return procgame.game.SwitchStop

    def sw_visor4_active(self,sw):
        if self.visor4<5:
            self.visor4+=1
            self.update_lamps_4()
        self.game.score(150*self.visor4)
        return procgame.game.SwitchStop

    def sw_visor5_active(self,sw):
        if self.visor5<5:
            self.visor5+=1
            self.update_lamps_5()
        self.game.score(150*self.visor5)
        return procgame.game.SwitchStop

    def sw_shooterLane_open_for_500ms(self,sw):
        self.game.coils.RvisorGI.schedule(schedule=0x0f0f0f0f, cycle_seconds=2, now=True)
        self.game.coils.LvisorGI.schedule(schedule=0xf0f0f0f0, cycle_seconds=2, now=True)
        self.game.effects.ramp_up()
        self.twoballsinplay = True

    def sw_outhole_active(self, sw):
        i=1
        while (i<=5):
            self.row_points(i)
            i+=1
        '''self.row_points(2)
        self.row_points(3)
        self.row_points(4)
        self.row_points(5)'''
        self.all_lamps_off()
        self.game.current_player().stop_eject_mode_mode(self)
        return procgame.game.SwitchStop
