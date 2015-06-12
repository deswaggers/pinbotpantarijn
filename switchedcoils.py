# -------------------------
# Switched Coils Control Mode - System 11
# myPinballs Jan 2014
#
# Copyright (C) 2013 myPinballs, Orange Cloud Software Ltd
# Aangepast Steven van der Staaij en Jelle Besseling voor Pinbot/Starwars
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# -------------------------

import time
from time import time
import procgame
import locale
import logging
from procgame import *


base_path = "C:\P-ROC\pyprocgame-master/"
game_path = "C:\P-ROC\pyprocgame-master\games\VXtra_start/"

class SwitchedCoils(game.Mode):

	def __init__(self, game, priority):
                super(SwitchedCoils, self).__init__(game, priority)

                self.ACCoilInProgress = False
                self.ACNameArray = ['outhole_knocker','trough','Ejecthole_LeftInsBFlash','Drops_RightInsBFlash','RampRaise_LowPlFlash','RampLow_EnergyFlash','Lejecthole_LeftPlFlash','Rejecthole_SunFlash']


        def mode_started(self):
            pass

        ############################
	#### AC Relay Functions ####
	############################
        
	def ACRelayEnable(self):
                self.game.coils.Solenoidselect.enable()
                self.ACCoilInProgress = False
                print 'nu weer enabled dus voor flashers'
        def test(self):
                self.game.coils.Solenoidselect.enable()
                self.ACCoilInProgress = False
                print 'nu weer enabled dus voor flashers'

	def acCoilPulse(self,coilname,pulsetime=50):
		### Setup variables ###
                self.game.coils.Solenoidselect.disable()
                self.coilname=coilname
                self.pulsetime=pulsetime
		self.ACCoilInProgress = True
		self.acSelectTimeBuffer = .3
		self.acSelectEnableBuffer = (pulsetime/1000)+(self.acSelectTimeBuffer*2)
                print self.acSelectEnableBuffer
		### Remove any scheduling of the AC coils ###
		for item in self.ACNameArray:
			self.game.coils[item].disable()

		### Stop any flashlamp lampshows
		#self.game.lampctrlflash.stop_show()

		### Start the pulse process ###
		self.cancel_delayed(name='acEnableDelay')
		self.coilfire()
		self.delay(name='coilDelay',event_type=None,delay=self.acSelectTimeBuffer,handler=self.game.coils[coilname].pulse,param=pulsetime)
		self.delay(name='acEnableDelay',delay=self.acSelectEnableBuffer,handler=self.ACRelayEnable)
		self.delay(name='coildelay_temp' , event_type=None, delay=self.acSelectEnableBuffer, handler=self.coilfire)
		
        def coilfire(self):
                self.game.coils[self.coilname].pulse(self.pulsetime)
                print 'nu moet spoel gaan'
                wait=20
                self.delay(name='test', event_type=None, delay=0.5, handler=self.test)
  
	def acFlashPulse(self,coilname,pulsetime=70):
                        self.game.coils.Solenoidselect.enable()
			self.game.coils[coilname].pulse(pulsetime)


	def acFlashSchedule(self,coilname,schedule=0x09090909,cycle_seconds=1.5,now=True):
                        self.game.coils.Solenoidselect.enable()
			self.game.coils[coilname].disable()
			self.game.coils[coilname].schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)


