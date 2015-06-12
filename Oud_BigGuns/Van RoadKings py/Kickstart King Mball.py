import procgame
from procgame import *
import random
from standaardzaken import *


class Multiball(game.Mode):

    def __init__(self, game, priority):
         super(Multiball, self).__init__(game, priority)

         self.log = logging.getLogger('rk.Multiball')

         self.lock_enabled = 0
         self.num_balls_locked = 0
         self.jackpotlit = 0
         self.timelock = 0
         self.multiball_score = 0
         self.game.current_player().multiballgestart+=1

         self.game.sound.register_sound('jackpot', voice_path+"jackpot - excited.wav")
         self.game.sound.register_sound('jackpotislit1', voice_path+"jackpot is lit.wav")
         self.game.sound.register_sound('jackpotislit2', voice_path+"shoot the right ramp.wav")
         self.game.sound.register_sound('superjackpotislit1', voice_path+"super jackpot is lit.wav")
         self.game.sound.register_sound('superjackpotislit2', voice_path+"shoot the super jackpot.wav")
         self.game.sound.register_sound('superjackpot1', sound_path+"Warning Siren.wav")
         self.game.sound.register_sound('superjackpot2', voice_path+"super jackpot.wav")
         self.game.sound.register_sound('ball1locked', voice_path+"jd - ball 1 captured.wav")
         self.game.sound.register_sound('ball2locked', voice_path+"jd - ball 2 locked.wav")
         self.game.sound.register_sound('bumper', sound_path+"gunshot.wav")


    def mode_started(self):
        super(Multiball, self).mode_started()
        self.game.trough.launch_balls(1)
        #self.game.trough.drain_callback = self.ball_drained_callback
        #self.game.trough.launch_balls(1, self.multiball_launch_callback)
        self.start_multiball()

    def mode_stopped(self):
        super(Multiball, self).mode_stopped()
        self.display_text(txt="Multiball total:", txt2=str(self.multiball_score), time=3)
        for lamp in self.game.lamps:
             lamp.disable()
        if self.game.switches.Leject.is_active():
            self.game.coils.Leject.pulse(16)
        if self.game.switches.Ceject.is_active():
            self.game.coils.Ceject.pulse(20)
        if self.game.switches.upperLkicker.is_active():
             self.ULkicker()
        self.cancel_delayed('kickout_Ceject')
        self.cancel_delayed('kickout_Leject')
        self.update_lamps_altijd()

#    def end_multiball(self):
#        self.end_callback()
#        self.update_lamps()

    def start_multiball(self):
        self.jackpotlit= 1
        self.update_lamps_multiball()

        gen = dmd.MarkupFrameGenerator()
        credits_frame = gen.frame_for_markup("""


#MULTIBALL#

[shoot ball to start]

[JACKPOT 1]
[Shoot right ramp]

[after jackpot]
[shoot left hole to light super jackpot]

[super jackpot is now lit]
[shoot centre ramp for super jackpot]

[shoot left hole to light normal jackpot again]

[shoot time locks to temporarily lock a ball]
[shoot both time locks in time to ad an extra ball]

[shoot ball]
[to start multiball]

""")

        self.credits_layer = dmd.PanningLayer(width=128, height=32, frame=credits_frame, origin=(0,0), translate=(0,1), bounce=False)

        script = [{'seconds':19.0, 'layer':self.credits_layer}]

        self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

        self.delay(name='updatelamps', event_type=None, delay=1, handler=self.update_lamps_multiball)

    def sw_ShooterLane_inactive_for_2s(self,sw):
        if self.timelock==0:
            self.ULkicker()
            self.layer=None
            x=random.random()
            if x>0.5:
                self.game.sound.play('jackpotislit1')
            else:
                self.game.sound.play('jackpotislit2')
        elif self.timelock==2:
              self.Ceject()
              self.Leject()

    def sw_bumperL_active(self,sw):
                self.bumper()
                return True

    def sw_bumperU_active(self,sw):
                self.bumper()
                return True

    def sw_bumperR_active(self,sw):
                self.bumper()
                return True

    def sw_bumperD_active(self,sw):
                self.bumper()
                return True

    def sw_slingL_active(self,sw):
                self.bumper()
                return True

    def sw_slingR_active(self,sw):
                self.bumper()
                return True

    def bumper(self):
         self.game.score(10)
         self.game.sound.play('bumper')

    def jackpot(self):
        if self.game.trough.num_balls_in_play == 3:
            self.game.score(1000000)
            self.multiball_score+=1000000
            x=random.random()
            if x>0.5:
                self.game.sound.play('superjackpot1')
            else:
                self.game.sound.play('superjackpot2')
        else:
           self.game.score(500000)
           self.multiball_score+=500000
           #self.rk_modes.show_on_display('JACKPOT!','None','low')
           #geluid en animatie
           self.game.sound.play('jackpot')

        self.game.lampctrl.play_show('modestart', False, 'None')
        self.showjackpot()
        self.jackpotlit=2
        self.game.current_player().aantal_jackpots+=1
        self.update_lamps_multiball()

    def superjackpot(self):
        if self.game.trough.num_balls_in_play == 3:
            self.game.score(2000000)
            self.multiball_score+=2000000
            x=random.random()
            if x>0.5:
                self.game.sound.play('superjackpot1')
            else:
                self.game.sound.play('superjackpot2')
        else:
            self.game.score(1000000)
            self.multiball_score+=1000000
            x=random.random()
            if x>0.5:
                self.game.sound.play('superjackpot1')
            else:
                self.game.sound.play('superjackpot2')
        self.game.lampctrl.play_show('modestart', False, 'None')
        anim = dmd.Animation().load(dmd_path+"superjackpot.dmd")
        self.play_animation(anim, 'high', repeat=False, hold=False)
        self.jackpotlit=0
        self.game.current_player().aantal_jackpots+=1
        self.game.coils.knocker_rampUp.pulse(30)
        self.update_lamps_multiball()

    def sw_RrampExit_active(self,sw):
        if self.jackpotlit==1:
            self.jackpot()
        #tijdelijk nog eens proberen met object rk_modes (in rk_modes.py erbij zetten/maken als object)
        self.delay(name='kickoutupperLkicker', event_type=None, delay=3, handler=self.ULkicker)
        return True

    def sw_CrampEnter_active(self,sw):
        if self.jackpotlit=='super':
            self.superjackpot()
        self.kickbackaantijdensmodes()
        #tijdelijk nog eens proberen met object rk_modes (in rk_modes.py erbij zetten/maken als object)

    def sw_Ceject_active(self,sw):
        return True

    def sw_Leject_active(self,sw):
        return True

    def sw_Leject_active_for_600ms(self,sw):
        self.kickbackaantijdensmodes()
        if self.jackpotlit==0:
            self.jackpotlit=1
            x=random.random()
            if x>0.5:
                self.game.sound.play('jackpotislit1')
            else:
                self.game.sound.play('jackpotislit2')
        elif self.jackpotlit==2:
            self.jackpotlit='super'
            if self.game.switches.dropTarget.is_active():
                self.droptargetup()
        if self.timelock==0:
            self.delay(name='kickout_Leject', event_type=None, delay=7, handler=self.kickout_Leject)
            self.timelock=1
            self.game.lamps.Ltimelock.enable()
            self.game.sound.play('ball1locked')
            self.show_on_display('Timelock 1', 'None', 'high')
        elif self.timelock==1:
            self.cancel_delayed('kickout_Ceject')
            self.game.score(50000)
            self.game.sound.play('ball2locked')
            self.show_on_display('Timelock 2', 'None', 'high')
            self.game.trough.launch_balls(1)
            self.timelock=2
        else:
            self.Leject()
            # geluid time locks gehaald!
            # hier het toevoegen van bal 3 aan de multiball?!
        self.update_lamps_multiball()
        return True

    def kickout_Leject(self):
        self.game.coils.Leject.pulse(16)
        self.timelock=0
        self.update_lamps_multiball()

    def showjackpot(self):
        anim = dmd.Animation().load(dmd_path+"jackpot.dmd")
        self.play_animation(anim, 'high', repeat=False, hold=False)

    def sw_dropTarget_active(self,sw):
        if self.jackpotlit=='super':
            x=random.random()
            if x>0.5:
                self.game.sound.play('superjackpotislit1')
            else:
                self.game.sound.play('superjackpotislit2')
        #return True

    def sw_Ceject_active_for_600ms(self,sw):
        if self.timelock==0:
            self.delay(name='kickout_Ceject', event_type=None, delay=10, handler=self.kickout_Ceject)
            self.timelock=1
            self.game.sound.play('ball1locked')
            self.show_on_display('Timelock 1', 'None', 'high')
            self.game.lamps.Ctimelock.enable()
        elif self.timelock==1:
            self.cancel_delayed('kickout_Leject')
            self.game.sound.play('ball2locked')
            self.show_on_display('Timelock 2', 'None', 'high')
            self.game.score(50000)
            self.game.trough.launch_balls(1)
            self.timelock=2
            # geluid time locks gehaald!
            # hier het toevoegen van bal 3 aan de multiball?!
        else:
            self.Ceject()
        self.update_lamps_multiball()
        #return True

    def kickout_Ceject(self):
        self.game.coils.Ceject.pulse(20)
        self.timelock=0
        self.update_lamps_multiball()

    def update_lamps_multiball(self):
        if self.jackpotlit==1:
            self.game.lamps.megaScore.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
            self.game.lamps.Rtimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
            self.game.lamps.Rlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=True)
            self.game.lamps.Rextraball.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
            self.drive_mode_lamp('stoplight_green','medium')
            self.drive_mode_lamp('stoplight_yellow','slow')
            self.drive_mode_lamp('stoplight_red','medium')
            self.game.lamps.Clock.disable()
            self.game.lamps.Llock.disable()
            self.game.lamps.detourWL.disable()
            self.game.lamps.Cextraball.disable()
            self.game.lamps.spotLetter.disable()
        elif self.jackpotlit=='super':
            self.game.lamps.megaScore.disable()
            self.game.lamps.Rtimelock.disable()
            self.game.lamps.Rlock.disable()
            self.game.lamps.Rextraball.disable()
            self.game.lamps.Llock.disable()
            self.drive_mode_lamp('stoplight_green','off')
            self.drive_mode_lamp('stoplight_yellow','off')
            self.drive_mode_lamp('stoplight_red','off')
            self.game.lamps.detourWL.schedule(schedule=0x00ffff00, cycle_seconds=0, now=True)
            self.game.lamps.Cextraball.schedule(schedule=0x000ffff0, cycle_seconds=0, now=True)
            self.game.lamps.spotLetter.schedule(schedule=0x0000ffff, cycle_seconds=0, now=True)
        elif self.jackpotlit==0 or self.jackpotlit==2:
            self.game.lamps.megaScore.disable()
            self.game.lamps.Rtimelock.disable()
            self.game.lamps.Rlock.disable()
            self.game.lamps.Rextraball.disable()
            self.drive_mode_lamp('Llock','medium')
            self.game.lamps.detourWL.disable()
            self.game.lamps.Cextraball.disable()
            self.game.lamps.spotLetter.disable()
            self.drive_mode_lamp('stoplight_green','off')
            self.drive_mode_lamp('stoplight_yellow','off')
            self.drive_mode_lamp('stoplight_red','off')

        if self.timelock==0:
            self.game.lamps.Ltimelock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=False)
            self.game.lamps.Ctimelock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=False)
        elif self.timelock==2 and not self.jackpotlit==0:
            self.drive_mode_lamp('Ltimelock','off')
            self.drive_mode_lamp('Ctimelock','off')
            self.update_lamps_altijd()
        print 'number balls in play=', self.game.trough.num_balls_in_play

