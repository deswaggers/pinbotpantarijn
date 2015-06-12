from procgame import *
from rk_modes import *
from standaardzaken import *

class Race2(Basiszaken):
        # alternatief: class Multiball(rk_modes.JD_Modes): ?
	def __init__(self, game, priority, font_small, font_big):
		super(Race2, self).__init__(game, priority)

		self.volgend_schot='Cramp'
                self.startracedoorflippers=1
                
		frenzy_switches = [self.game.switches.targetR, self.game.switches.targetO,self.game.switches.targetA,self.game.switches.targetD, self.game.switches.outlaneR, self.game.switches.droptarget,self.game.switches.Rtenpoint,self.game.switches.Ltenpoint]
                for sw in frenzy_switches:
                        self.add_switch_handler(sw.name, 'active', 0, self.frenzy_switch_active)

                # Gerry's aanvulling:
                #for switch in self.game.switches:
                #        self.add_switch_handler(...)

	def mode_started(self):
                super(Race2, self).mode_started()
                for lamp in self.game.lamps:
			lamp.disable()
                self.game.sound.register_sound('stapterug', voice_path+"DH time flies when.wav")
                self.game.sound.register_sound('stapvooruit', voice_path+"DH you've been practising.wav")
                self.game.sound.register_sound('stapvooruit2', voice_path+"DH now that's shootingh.wav")
                self.game.sound.register_sound('hurry', voice_path+"DH Hurry.wav")
                self.game.sound.register_music('race2', music_path+"mainSongLoop.mp3")
                self.game.sound.register_sound('just in time', voice_path+"DH just in timeh.wav")

                self.game.sound.play_music('race2', loops=-1)
                	
                gen = dmd.MarkupFrameGenerator()
		credits_frame = gen.frame_for_markup("""


#RULES RACE 2#

[Winning the race DOUBLES your score!!!!]

[press flippers to start ]


[Shoot the flashing shot]

[If a shot is made, you'll progress one shot to the right]

[If a shot is not made, you'll fall behind]

[Shooting the shots in time, wins the race]

[Not making the required shots, will lose the race]

[Loosing the race, will drain the ball, but it'll not cost you your ball]

[Winning the race makes you champion of race 2]

[Winning the race DOUBLES your score!!!!]


[press both flippers]
[to start race 2]

""")

		self.credits_layer = dmd.PanningLayer(width=128, height=32, frame=credits_frame, origin=(0,0), translate=(0,1), bounce=False)

                script = [{'seconds':28.0, 'layer':self.credits_layer}]

		self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)
		
                self.update_lamps_race2()
                self.delay(name='updatelamps', event_type=None, delay=1, handler=self.update_lamps_race2)

 
	def mode_stopped(self):
                super(Race2, self).mode_stopped()
                for lamp in self.game.lamps:
			lamp.disable()
		self.game.sound.fadeout_music()

		
        def sw_flipperLwL_active(self, sw):
                if self.game.switches.flipperLwR.is_active() and self.startracedoorflippers==1 and self.game.switches.upperLkicker.is_active():
                        self.startracedoorflippers=0
                        self.cancel_delayed(name='start_race2')
                        self.layer=None
                        self.start_race2()
        def sw_flipperLwR_active(self, sw):
                if self.game.switches.flipperLwL.is_active() and self.startracedoorflippers==1 and self.game.switches.upperLkicker.is_active():
                        self.startracedoorflippers=0
                        self.cancel_delayed(name='start_race2')
                        self.layer=None
                        self.start_race2()
                        
        def play_animation(self):
             anim = dmd.Animation().load(dmd_path+'arrows_ttt.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=3)
             #self.animation_layer.add_frame_listener(-1, self.clear_layer)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.combo_text, self.info_text])
             self.delay(name='clear_display', event_type=None, delay=3.5, handler=self.clear_layer)


        def start_race2(self):
                self.delay(name='schotterug', event_type=None, delay=8, handler=self.schotterug)
                self.ULkicker()
                self.game.kickbackaan=1
                self.update_lamps_race2()
                self.delay(name='updatelamps', event_type=None, delay=1, handler=self.update_lamps_race2)
                


        def schotterug(self):
                if self.volgend_schot=='Rramp':
                        self.volgend_schot='Rramp5sec'
                elif self.volgend_schot=='Cramp':
                        self.volgend_schot='Cramp5sec'
                elif self.volgend_schot=='Lkickouthole':
                        self.volgend_schot='Lkickouthole5sec'
                elif self.volgend_schot=='Lloop':
                        self.volgend_schot='Lloop5sec'
                elif self.volgend_schot=='Ckickouthole':
                        self.volgend_schot='Ckickouthole5sec'

                self.delay(name='schotterug2', event_type=None, delay=4, handler=self.schotterug2)
                self.game.sound.play('DH Hurry')        
                self.update_lamps_race2()
                
        def schotterug2(self):
                if self.volgend_schot=='Cramp5sec':
                        self.volgend_schot='Lkickouthole'
                elif self.volgend_schot=='Lkickouthole5sec':
                        self.volgend_schot='Lloop'
                        if self.game.switches.rampraise.is_active():
                                self.game.coils.solenoidselectrelais.pulse(40)
                                self.game.coils.knocker_rampup.pulse(36) 
                elif self.volgend_schot=='Lloop5sec':
                        for lamp in self.game.lamps:
                                lamp.disable()
                        self.game.coils.GIrelay.schedule(0xffffffff, cycle_seconds=3, now=True)
                        self.game.coils.flipperenable.disable()
                        self.game.current_player().extra_balls += 1
                        self.show_on_display('Race lost. Ball saved though.','klein','mid')
                        # self.delay(name='mode-eindigen', event_type=None, delay=6, handler=self.game.modes.remove, param1=self)
                        # alternatief: self.game.modes.remove(self) oid?
                        # NU TOCH GEWOON IN outhole gedaan bij rk_modes!
                elif self.volgend_schot=='Ckickouthole5sec':
                        self.volgend_schot='Cramp'
                elif self.volgend_schot=='Rramp5sec':
                        self.volgend_schot='Ckickouthole'

                self.delay(name='schotterug', event_type=None, delay=7, handler=self.schotterug)
                self.game.sound.play('stapterug')                        
                self.update_lamps_race2()
                # steeds1n schot vooruit als je een schot hebt gemaakt. Positie aan de hand daarvan? plaats 1 t/m 5 oid?
                # na een tijdje 1 schot/positie terug
                # tijd aangeven door 'snelheid' van knipperende lampjes? Snel knipperend, bijna 1 positie terug? Daarbij ook 'er zit er 1 vlak achter je'
                # en 'mooie inhaalmaneuvre' oid?

                # Alternatief: Goede schot 1 plek vooruit, slecht schot 1 plek achteruit!

        def frenzy_switch_active(self, sw):
                self.frenzy_score()
                return True
        def sw_bumperL_active(self,sw):
                self.frenzy_score()
                return True
	def sw_bumperU_active(self,sw):
                self.frenzy_score()
                return True
	def sw_bumperR_active(self,sw):
                self.frenzy_score()
                return True
	def sw_bumperD_active(self,sw):
                self.frenzy_score()
                return True
        def sw_slingL_active(self,sw):
                self.frenzy_score()
                return True
        def sw_slingR_active(self,sw):
                self.frenzy_score()
                return True        
	def frenzy_switch_active(self, sw):
                self.frenzy_score()
                return True
        def frenzy_score(self):
                self.game.score(10)
                return True

        def sw_Lrollunder_active(self,sw):
                if self.volgend_schot=='Lloop5sec' or self.volgend_schot=='Lloop':
                        self.volgend_schot='Lkickouthole'
                        self.stap_vooruit()
                        self.game.sound.play('just in time')
                        #self.show_on_display('Shoot left hole','None','mid')
                self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                return True

        def sw_Leject_active(self,sw):
                if self.volgend_schot=='Lkickouthole5sec' or self.volgend_schot=='Lkickouthole':
                        self.volgend_schot='Cramp'
                        self.stap_vooruit()
                        #self.show_on_display('Shoot center ramp','None','mid')
                self.kickbackaan()
                self.game.coils.Lejecthole.pulse(20)
                return True

        def sw_Crampenter_active(self,sw):
                if self.volgend_schot=='Cramp5sec' or self.volgend_schot=='Cramp':
                        self.volgend_schot='Ckickouthole'
                        self.stap_vooruit()
                        #self.show_on_display('Shoot right hole','None','mid')
                self.kickbackaantijdensmodes()
                self.delay(name='kickbackaantijdensmodes', event_type=None, delay=3, handler=self.kickbackaantijdensmodes)
                self.game.lamps.kickback.schedule(schedule=0xf0f0f0f0, cycle_seconds=3, now=True)
                return True




        def sw_Ceject_active(self,sw):
                if self.volgend_schot=='Ckickouthole5sec' or self.volgend_schot=='Ckickouthole':
                        self.volgend_schot='Rramp'
                        self.stap_vooruit()
                        #self.show_on_display('Shoot ramp','None','mid')
                        if self.game.switches.rampraise.is_inactive():
                                self.game.coils.solenoidselectrelais.pulse(30)
                                self.game.coils.midinsertboardflashers_rampdown.pulse(25)
                self.game.coils.Cejecthole.pulse(20)
                return True

        def stap_vooruit(self):
                self.cancel_delayed('schotterug')
                self.cancel_delayed('schotterug2')
                self.delay(name='schotterug', event_type=None, delay=5, handler=self.schotterug)
                anim = dmd.Animation().load(dmd_path+"tomcat3.dmd")
		self.play_animation(anim, 'high', repeat=False, hold=False)
		self.game.score(100000)
                x=random.random()
                if x>0.5:
                        self.game.sound.play('stapvooruit')
                else:
                        self.game.sound.play('stapvooruit2')
                self.update_lamps_race2()
        
        def sw_Rrampexit_active(self,sw):
                if self.volgend_schot=='Rramp5sec' or self.volgend_schot=='Rramp':
                        self.cancel_delayed('schotterug')
                        self.cancel_delayed('schotterug2')
                        for lamp in self.game.lamps:
                                lamp.disable()
                        self.game.current_player().race2_gewonnen=1
                        self.game.coils.GIrelay.schedule(0xffffffff, cycle_seconds=3, now=True)
                        self.game.coils.flipperenable.disable()
                        x=self.game.current_player().score
                        self.game.current_player().score+=x
                        self.show_on_display('Race won. You doubled your score: now 2x.', x,'mid')
                        #self.game.current_player().extra_balls += 1
                #Animatie overwinning, geluid overwinning, lampshow. Bal wegschieten, laten drainen en totale bonus en dergelijke laten zien en nieuwe bal geven.
                self.delay(name='kickoutupperLkicker', event_type=None, delay=3, handler=self.ULkicker)
                return True
                
	def update_lamps_race2(self):
                for lamp in self.game.lamps:
                        lamp.disable()
                if self.volgend_schot=='Lkickouthole':
                        self.game.lamps.Ltimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                        self.game.lamps.Llock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Lkickouthole5sec':
                        self.game.lamps.Ltimelock.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                        self.game.lamps.Llock.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Cramp':
                        self.game.lamps.spotletter.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                        self.game.lamps.Cextraball.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Cramp5sec':
                        self.game.lamps.spotletter.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                        self.game.lamps.Cextraball.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Lloop':
                        self.game.lamps.bonusholdWL.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Lloop5sec':
                        self.game.lamps.bonusholdWL.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Ckickouthole5sec':
                        self.game.lamps.Clock.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                        self.game.lamps.Ctimelock.schedule(schedule=0x88888888, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Ckickouthole':
                        self.game.lamps.Clock.schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                        self.game.lamps.Ctimelock.schedule(schedule=0xf0f0f0f0, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Rramp5sec':
                        self.game.lamps.Rtimelock.schedule(schedule=0x80808080, cycle_seconds=0, now=True)
                        self.game.lamps.Rlock.schedule(schedule=0x08080808, cycle_seconds=0, now=True)
                        #self.game.lamps.Rextraball.schedule(schedule=0x80808080, cycle_seconds=0, now=True)
                elif self.volgend_schot=='Rramp':
                        self.game.lamps.Rtimelock.schedule(schedule=0xf00f00f0, cycle_seconds=0, now=True)
                        self.game.lamps.Rlock.schedule(schedule=0x0f00f00f, cycle_seconds=0, now=True)
                        #self.game.lamps.Rextraball.schedule(schedule=0x00f00f00, cycle_seconds=0, now=True)

                self.update_lamps_altijd()
