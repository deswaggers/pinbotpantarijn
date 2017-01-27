# Effects
#
# Basic mode for general effects and control of game items (lamps, coils, etc.)

import procgame
import locale
from procgame import *
import time

game_path = game_path = "/home/pi/VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"

class Effects(game.Mode):

    def __init__(self, game):
        super(Effects, self).__init__(game, 4)
        self.game.sound.register_sound('ramp_up', sound_path+"rampup.wav")

    # Lamp effects (eerste, de drive_lamp_schedule' kan weg als we die nergens aanroepen)

    def drive_lamp_schedule(self, lamp_name, schedule=0x0f0f0f0f, cycle_seconds=0, now=True):
        self.game.lamps[lamp_name].schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)

    def drive_lamp(self, lamp_name, style='on',time=2):
        if style == 'slow':
            self.game.lamps[lamp_name].schedule(schedule=0x00ff00ff, cycle_seconds=0, now=True)
        elif style == 'medium':
            self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
        elif style == 'fast':
            self.game.lamps[lamp_name].schedule(schedule=0x44444444, cycle_seconds=0, now=True)
        elif style == 'superfast':
            self.game.lamps[lamp_name].schedule(schedule=0x93939393, cycle_seconds=0, now=True)
        elif style == 'on':
            self.game.lamps[lamp_name].enable()
        elif style == 'off':
            self.game.lamps[lamp_name].disable()
            # also cancel any pending delays
            self.cancel_delayed(lamp_name+'_medium')
            self.cancel_delayed(lamp_name+'_fast')
            self.cancel_delayed(lamp_name+'_superfast')
        elif style == 'smarton':
            self.game.lamps[lamp_name].schedule(schedule=0xaaaaaaaa, cycle_seconds=0, now=True)
            self.delay(name=lamp_name+'_on', event_type=None, delay=0.6, handler=self.game.lamps[lamp_name].enable)
        elif style == 'smartoff':
            self.game.lamps[lamp_name].schedule(schedule=0xaaaaaaaa, cycle_seconds=0, now=True)
            self.delay(name=lamp_name+'_off', event_type=None, delay=0.6, handler=self.game.lamps[lamp_name].disable)
        elif style == 'timeout':
            self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
            if time>10:
                self.delay(name=lamp_name+'_medium', event_type=None, delay=time-10, handler=self.drive_medium, param=lamp_name)
            if time>5:
                self.delay(name=lamp_name+'_fast', event_type=None, delay=time-5, handler=self.drive_fast, param=lamp_name)
            if time>1:
                self.delay(name=lamp_name+'_superfast', event_type=None, delay=time-1, handler=self.drive_super_fast, param=lamp_name)
            self.delay(name=lamp_name+'_off', event_type=None, delay=time, handler=self.game.lamps[lamp_name].disable)

    def drive_super_fast(self, lamp_name):
        self.game.lamps[lamp_name].schedule(schedule=0x99999999, cycle_seconds=0, now=True)

    def drive_fast(self, lamp_name):
        self.game.lamps[lamp_name].schedule(schedule=0x55555555, cycle_seconds=0, now=True)

    def drive_medium(self, lamp_name):
        self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)


    #Flashers standaard-aansturing: nog beter uit te werken
    def drive_flasher(self, data, style='medium',cycle=0,time=2):
        if isinstance(data, basestring):
            flasher_name=data
        else:
            flasher_name=data[0]
            style = data[1]
            time = data[2]


        if style == 'slow':
            self.game.coils[flasher_name].schedule(schedule=0x00003000, cycle_seconds=cycle, now=True)
        elif style == 'medium':
            self.game.coils[flasher_name].schedule(schedule=0x30003000, cycle_seconds=cycle, now=True)
        elif style == 'fast':
            self.game.coils[flasher_name].schedule(schedule=0x11111111, cycle_seconds=cycle, now=True)
        elif style == 'super':
            self.game.coils[flasher_name].schedule(schedule=0x55555555, cycle_seconds=cycle, now=True)
        elif style == 'super2':
            self.game.coils[flasher_name].schedule(schedule=0x55055055, cycle_seconds=cycle, now=True)
        elif style == 'strobe':
            self.game.coils[flasher_name].schedule(schedule=0xeeeeeeee, cycle_seconds=cycle, now=True)
        elif style == 'chaos':
            self.game.coils[flasher_name].schedule(schedule=0x019930AB, cycle_seconds=cycle, now=True)
        elif style == 'fade':
            self.game.coils[flasher_name].schedule(schedule=0xAAA99933, cycle_seconds=cycle, now=True)

        if time>0:
            self.delay(name=flasher_name+'_off', event_type=None, delay=time, handler=self.game.coils[flasher_name].disable)


    def strobe_flasher_set(self,flasher_list,time=1,overlap=0.2,repeats=1,enable=True):
        timer = 0
        for i in range(repeats):
            for fname in flasher_list:
                if enable:
                    self.delay(name=fname+'strobe', event_type=None, delay=timer, handler=self.drive_flasher, param=[fname,'fast',time+overlap])
                    timer+=time
                else:
                    self.cancel_delayed(fname+'strobe')
                    self.game.coils[fname].disable()


    def strobe_controlled_flasher_set(self,flasher_list,time=0.1,overlap=0.2,repeats=1,enable=True):
        pass
    ##            timer = 0
    ##
    ##            #playfield flashers
    ##            sequence=[]
    ##            for j in range(repeats):
    ##                sequence += flasher_list
    ##
    ##            for i in range(len(sequence)):
    ##
    ##                def flash(i,time,delay):
    ##                    self.delay(delay=delay,handler=lambda:self.game.switchedCoils.drive(name=sequence[i],style='fast',time=time+0.1))
    ##
    ##                flash(i,time,timer)
    ##                timer+=time

    # General Illumination:
    def gi_on(self):
        self.game.coils.GIPlayfield.disable()
        self.game.coils.GIInsB.disable()
        self.game.coils.RvisorGI.disable()

    def gi_off(self):
        self.game.coils.GIPlayfield.pulse(0)
        self.game.coils.GIInsB.pulse(0)
        self.game.coils.RvisorGI.pulse(0)

    def gi_blinking(self, schedule=0x0f0f0f0f, cycle_seconds=1, now=True):
        self.game.coils.GIPlayfield.schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)
        self.game.coils.GIInsB.schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)
        self.game.coils.RvisorGI.schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)

    # AC-Select coils: ramp en droptargets in functie / method gezet

    def ramp_up(self):
        if self.game.switches.rampdown.is_active():
            self.game.switchedCoils.acCoilPulse('RampRaise_LowPlFlash')
            self.game.sound.play("ramp_up")
            print 'rampup'
    def ramp_down(self):
        if self.game.switches.rampdown.is_inactive():
            self.game.switchedCoils.acCoilPulse('RampLow_EnergyFlash')
            print 'rampdown'
    def drops_reset(self):
        self.game.switchedCoils.acCoilPulse('Drops_RightInsBFlash',90)



    #Laat diverse flashers even 'flashen', daaronder voor andere flashers, waarbij energy_flash gaat flashen totdat ie gestopt wordt
    def flashers_flash(self, time=1):
        self.game.coils.Solenoidselect.schedule(schedule=0xffffffff, cycle_seconds=time, now=False)
        self.game.coils.trough.schedule(schedule=0xf00f00f0, cycle_seconds=time, now=False)
        self.game.coils.RampRaise_LowPlFlash.schedule(schedule=0x0f00f00f, cycle_seconds=time, now=False)
        self.game.coils.Lejecthole_LeftPlFlash.schedule(schedule=0x00f00f00, cycle_seconds=time, now=False)
        self.game.coils.Rejecthole_SunFlash.schedule(schedule=0x0f00f00, cycle_seconds=time, now=False)
    def lower_flashers_flash(self, time=1):
        self.game.switchedCoils.acFlashSchedule('RampRaise_LowPlFlash', cycle_seconds=2)
    def energy_flash(self, time=1):
        self.game.switchedCoils.acFlashSchedule('RampLow_EnergyFlash', cycle_seconds=1)

    def upperPlayfield_flash(self, time=1):
        self.game.coils.Solenoidselect.schedule(schedule=0xffffffff, cycle_seconds=time, now=False)
        self.game.coils.trough.schedule(schedule=0x0f00f080, cycle_seconds=time, now=False)
    def leftPlayfield_flash(self, time=1):
        self.game.coils.Solenoidselect.schedule(schedule=0xffffffff, cycle_seconds=time, now=False)
        self.game.coils.Lejecthole_LeftPlFlash.schedule(schedule=0x00f00f00, cycle_seconds=time, now=False)



    # Ball control

    def flippers(self, flip_on=True):
        if flip_on:
            self.game.coils.flipperEnable.enable()
        else:
            self.game.coils.flipperEnable.disable()

    def release_stuck_balls(self):
        #outhole
        if self.game.switches.outhole.is_active():
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
        if self.game.switches.visorOpen.is_active():
            self.delay(name='visor_closing' , event_type=None, delay=3, handler=self.game.visor_up_down.visor_move)
        if self.game.switches.droptarget1.is_active() or self.game.switches.droptarget2.is_active() or self.game.switches.droptarget3.is_active():
            self.game.coils.Drops_RightInsBFlash.pulse(100)
        self.eject_ball()

    def throw_ball_delay(self):
        self.delay(name='throw_ball' , event_type=None, delay=0.4, handler=self.game.coils.trough.pulse(55))

    def eject_ball(self, location='all'):
        #self.game.coils.Solenoidselect.disable()
        #left eject
        if location == 'all' or location == 'Leject':
            if self.game.switches.Leject.is_active():
                self.game.switchedCoils.acCoilPulse('Lejecthole_LeftPlFlash')
                #self.game.coils.Lejecthole_LeftPlFlash.pulse(22)

        #center eject
        if location == 'all' or location == 'Reject':
            if self.game.switches.Reject.is_active():
                self.game.switchedCoils.acCoilPulse('Rejecthole_SunFlash')
                #self.game.coils.Rejecthole_SunFlash.pulse(24)

        #upper left kicker
        if location == 'all' or location == 'eject':
            if self.game.switches.eject.is_active():
                self.game.switchedCoils.acCoilPulse('Ejecthole_LeftInsBFlash')
                print 'eject gedaan'
                #self.game.coils.Ejecthole_LeftInsBFlash.pulse(40)

            # Deze laat ik even staan omdat er misschien elders in de code naar verwezen wordt. Later weg te halen en alleen 'release_stuck_balls' gebruiken
    def ball_search(self):
        self.release_stuck_balls()


