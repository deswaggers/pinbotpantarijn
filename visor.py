# Visor

 from procgame import *
from multiball import *

# all paths
game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
lampshow_path = game_path +"lampshows/"

class Visor(game.Mode):

        def __init__(self, game, priority):
                super(Visor, self).__init__(game, priority)
                self.game.lampctrl.register_show('lampshow_visor' ,lampshow_path +"Pinbot_1.lampshow")


        def mode_started(self):
                print "visor_mode started"
                self.colors = ['yellow', 'blue', 'orange', 'green', 'red']
                self.game.lampctrl.play_show('lampshow_visor', repeat=True)
                self.multiball = Multiball(self.game, 40)
                self.game.current_player().visor_position='down' #dit wordt niet meer gebruikt
                self.update_lamps()
##                self.multiball.callback = self.mode_callback

        def mode_stopped(self):
                self.game.lampctrl.stop_show()


##        def mode_callback(self,mode_name):
##             #remove the active mode
##             print("Ending Mode: "+mode_name)
##             if mode_name == 'multiball':
##                  self.game.modes.remove(self.multiball)

## switches
        def update_visor(self, num):
                 self.game.lampctrl.stop_show()
                 self.game.sound.play("sound_lasergun2")
                 self.game.score(10)
                 if self.game.current_player().visor_lamps[num] < 5:
                         self.game.current_player().visor_lamps[num] += 1
                         self.game.sound.play("sound_visor_hit")
                 else:
                         self.game.sound.play("sound_visor_full")
                 self.update_lamps()
                 print "Visor", num , "is nu:", self.game.current_player().visor_lamps[num]

        def sw_visor1_active(self,sw):
             self.update_visor(0)

        def sw_visor2_active(self,sw):
             self.update_visor(1)

        def sw_visor3_active(self,sw):
             self.update_visor(2)

        def sw_visor4_active(self,sw):
             self.update_visor(3)

        def sw_visor5_active(self,sw):
             self.update_visor(4)

        def sw_Rbank1_active(self,sw):
             self.update_visor(0)

        def sw_Rbank2_active(self,sw):
             self.update_visor(1)

        def sw_Rbank3_active(self,sw):
             self.update_visor(2)

        def sw_Rbank4_active(self,sw):
             self.update_visor(3)

        def sw_Rbank5_active(self,sw):
             self.update_visor(4)

        def sw_visorClosed_active(self,sw):
                print "Visor closed"
                self.game.coils.Visormotor.disable()

        def stop_visor(self):
                self.game.coils.Visormotor.disable()

        def sw_visorOpen_active(self,sw):
                self.delay(name='visor_stop' , event_type=None, delay=0.8, handler=self.stop_visor)

        def sw_Leject_active_for_100ms(self,sw):
                if not self.game.switches.Reject.is_active():
                        self.game.trough.launch_balls(1)
                        self.game.current_player().mode_running = True
                        self.game.effects.ramp_down()
                        #self.game.switchedCoils.acCoilPulse('trough')
##                        self.game.coils.trough.pulse(50)
                else:
                        self.delay(name='start_mb' , event_type=None, delay=1, handler=self.start_multiball)
                        self.update_lamps()

        def sw_Reject_active_for_100ms(self,sw):
                if not self.game.switches.Leject.is_active():
                        self.game.trough.launch_balls(1)
                        self.game.current_player().mode_running = True
                        self.game.effects.ramp_down()
                        #self.game.switchedCoils.acCoilPulse('trough')
##                        self.game.coils.trough.pulse(50)
                else:
                        self.delay(name='start_mb' , event_type=None, delay=1, handler=self.start_multiball)
                        self.update_lamps()

## Lampen

        def update_lamps(self):
                if sum(self.game.current_player().visor_lamps) == 25:
                        print ("25 visor lamps!")
                        self.game.current_player().visor_position='up'
                if sum(self.game.current_player().visor_lamps) == 25 and self.game.switches.visorClosed.is_active():
                        self.game.sound.play("sound_visor_down")
                        self.game.visor_up_down.visor_move()
                        self.game.current_player().visor_lamps = [0,0,0,0,0]
                #elif sum(self.game.current_player().visor_lamps) != 25 and not self.game.switches.visorClosed.is_active():
                #        self.game.visor_up_down.visor_move()
                #        pass
                for x in range(len(self.game.current_player().visor_lamps)):
                        for y in range(self.game.current_player().visor_lamps[x]):
                                self.game.effects.drive_lamp(self.colors[x] + str(y+1), 'on')


## Mode functions
        def start_multiball(self):
               self.game.modes.add(self.multiball)
