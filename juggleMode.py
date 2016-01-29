# Control for main modes
#

import procgame
import random
from procgame import *


#all necessary paths
game_path ="/home/pi/VXtra_start/"
dmd_path = game_path +"dmd/"

class JuggleMode(game.Mode):

    def __init__(self, game, priority):
        super(JuggleMode, self).__init__(game, priority)            
        self.yellow = ["yellow1", "yellow2", "yellow3", "yellow4", "yellow5"]
        self.blue = ["blue1", "blue2", "blue3", "blue4", "blue5"]
        self.orange = ["orange1", "orange2", "orange3", "orange4", "orange5"]
        self.green = ["green1", "green2", "green3", "green4", "green5"]
        self.red = ["red1", "red2", "red3", "red4", "red5"]

    def mode_started(self):        
            self.multiplier=1
            self.modescore=0
            self.kant = True
            self.update_lamps()  
            self.text_layer = dmd.TextLayer(5, 20, self.game.fonts['num_09Bx7'], "left", opaque=False)
            #self.game.lampctrl.register_show('rk_ramp_ready', lampshow_path+"ramp_ready.lampshow")

    # def sw_eject_active_for_500ms(self, sw):
    #         if self.game.current_player().mode_running==False:
    #                 self.game.score(2500)
    #                 self.game.current_player().mode_running=True
    #         else:
    #                 self.game.score(2500)
    #         self.update_lamps()
            
    def update_lamps(self):
        # if self.game.current_player().mode_running==False:
        #     self.game.effects.drive_lamp('eject0','medium')
        # else:
        #     self.game.effects.drive_lamp('eject0','off')
        if self.kant==True:
            verticaal_aan4()
            verticaal_aan5()
            verticaal_uitTrue()
            verticaal_uit2()
        else:
            verticaal_aanTrue()
            verticaal_aan2()
            verticaal_uit4()
            verticaal_uit5()
        self.text_layer.set_text(str(self.modescore), 1, 20)
        
    


    def echte_start(self):
        if self.game.switches.visorOpen.is_active():
            self.game.effects.visor_up_down.visor_move()
        
        self.kant=False #Linkertwee lichtjes gaan aan, links=False, rechts=True
        self.update_lamps()
    
    #Stopt de mode
    def sw_outhole_active(self,sw):
        self.game.score(self.multiplier*self.modescore)
        self.game.modes.remove(self)

    
    def sw_visor1_active(self, sw):
        is_hit(False)
    def sw_visor2_active(self, sw):
        is_hit(False)
    def sw_visor4_active(self, sw):
        is_hit(True)
    def sw_visor5_active(self, sw):
        is_hit(True)
    
    def is_hit(self,index):
        if index==self.kant:
            self.kant=not self.kant
            update_lamp()
            self.modescore+=1000
            self.multiplier+=0.5
            if self.multiplier==2:
                self.game.trough.launch_balls(1)
                self.modescore+=1000
            
        
    def verticaal_aan1(self):
        for i in self.yellow:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan2(self):
        for i in self.blue:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan3(self):
        for i in self.orange:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan4(self):
        for i in self.green:
            self.game.effects.drive_lamp(i, 'medium')

    def verticaal_aan5(self):
        for i in self.red:
            self.game.effects.drive_lamp(i, 'medium')

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

    #Hoi elbun hoeist