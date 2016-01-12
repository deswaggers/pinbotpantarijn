# General play
# allerlei import: niet alles is nodig of wordt gebruikt: later op te schonen

import random
import procgame
import locale
import logging
from os import listdir, walk
from os.path import join, splitext
from time import time
from random import randint
from procgame import *

# Dit importeert alle regels tijdens het gewone spel. Modes worden in ejectmodestart gestart.
from ejectmodestart import *
from bumpers import *
from visor import *
from droptargets import *

# all paths
game_path = "/home/pi/VXtra_start/"
plugin_dir = game_path+"plugins/"
speech_path = game_path+"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"
supported_sound = ['.wav', '.aiff', '.ogg', '.mp3']

class Generalplay(game.Mode):

    def __init__(self, game, priority):
        super(Generalplay, self).__init__(game, priority)

        # register modes: hij maakt van de code die onder 'visor_rules' staat een object. Het nummer gaat over prioriteit die bv belangrijk is voor animaties:
        # Hogere prioriteit wordt als eerste behandeld, dus een 'mode' die voorrang heeft
        # op het normale spel moet hoger zijn, hieronder daarom voor 9,10,11,12 gekozen.
        self.ejectModestart_rules = EjectModestart(self.game, 9)
        self.bumper_rules = Bumpers(self.game, 10)
        # self.visor_rules = Visor(self.game, 11)
        self.droptarget_rules = Droptargets(self.game, 12)


        self.game.current_player().mode_lamps = 0


        ## Modestart straks naar elders, veel zaken in general_play nog op te schonen.
        #self.modes = [None, Mode1 (self.game, 19), Mode2 (self.game, 18), Mode3(self.game, 70)]
        #self.register_all_plugins()

        self.register_all_sounds()
        self.game.lampctrl.register_show('rampenter_show', lampshow_path+"rampenter.lampshow")


    def reset(self):
        pass

    def mode_started(self):

        startanim = dmd.Animation().load(dmd_path+'intro_starwars.dmd')

        self.game.modes.add(self.ejectModestart_rules)

        self.game.modes.add(self.bumper_rules)
        # self.game.modes.add(self.visor_rules)
        self.game.modes.add(self.droptarget_rules)

        if self.game.ball==1:
            self.animation_layer = dmd.AnimatedLayer(frames=startanim.frames, opaque=False, repeat=False, hold=False, frame_time=1)
            self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
            self.delay(name='clear_layer', event_type=None, delay=4, handler=self.clear_layer)
        self.game.sound.play_music('music_starwars_intro', loops=-1)
        self.game.sound.play('speech_Prepare_to_fire')
        self.game.effects.ramp_down()
        print "general play gestart"

    def clear_layer(self):
        self.layer = None

    def start_mode(self, index):
        if not self.game.current_player().mode_running:
            self.game.current_player().mode_running = index
            self.game.modes.add(self.modes[index])
            if self.game.current_player().mode_lamps < 10:
                self.game.current_player().mode_lamps += 1
            self.update_lamps()
        else:
            print "Mode", index, "werd geprobeerd te starten maar", self.game.current_player().mode_running, "draait al"

    def start_mode_random(self):
        print "Start random mode"
        self.start_mode(randint(1, len(self.modes)-1))

    def register_all_plugins(self):
        modes = []
        for file in listdir(plugin_dir):
            if splitext(file)[1] == '.py':
                modes.append(splitext(file)[0])
        for mode in modes:
            print "REGISTER MODE:", mode
            self.modes.append(getattr(__import__('.plugins', globals(), locals(), [mode]), mode).Mode(self.game))

    def register_all_sounds(self):
        # Register all sounds!
        for (dirpath, dirnames, filenames) in walk(speech_path):
            for filename in filenames:
                if splitext(filename)[1] in supported_sound:
                    sound = "speech_" + splitext(filename)[0].replace(" ", "_")
                    print "SOUND REGISTERED:", sound
                    self.game.sound.register_sound(sound, join(dirpath, filename))

        for (dirpath, dirnames, filenames) in walk(sound_path):
            for filename in filenames:
                if splitext(filename)[1] in supported_sound:
                    sound = "sound_" + splitext(filename)[0].replace(" ", "_")
                    print "SOUND REGISTERED:", sound
                    self.game.sound.register_sound(sound, join(dirpath, filename))

        for (dirpath, dirnames, filenames) in walk(music_path):
            for filename in filenames:
                if splitext(filename)[1] in supported_sound:
                    sound = "music_" + splitext(filename)[0].replace(" ", "_")
                    print "SOUND REGISTERED:", sound
                    self.game.sound.register_music(sound, join(dirpath, filename))

    def mode_stopped(self):
        self.game.modes.remove(self.ejectModestart_rules)
        self.game.modes.remove(self.bumper_rules)
        # self.game.modes.remove(self.visor_rules)
        self.game.modes.remove(self.droptarget_rules)

        print 'generalplay stopped'

    def mode_tick(self):
        pass

## lamps and animations

    def update_lamps(self):
        if self.game.current_player().mode_lamps < 9:
            #pass #de sun moet dan flashen
            # @Jelle: hier even in de if gezet
            for x in range(self.game.current_player().mode_lamps):
                self.game.effects.drive_lamp('planet' + str(x+1), 'on')
                if x < 9:
                    self.game.effects.drive_lamp('planet' + str(x+2), 'medium')
        #Steven (ook kan: if self.game.ramp_move.ramp_up:
        # wel gaan hier problemen komen met modes: als die ook de lampjes willen aansturen....daarnaast gaat de lampupdate niet vaak genoeg
        if self.game.current_player().mode_running:
            self.game.effects.drive_lamp('advance_planet','medium')
        else:
            self.game.effects.drive_lamp('advance_planet','off')



## Switches regular gameplay
    def sw_shooterLane_open_for_100ms(self,sw):
        self.game.coils.RvisorGI.schedule(schedule=0x0f0f0f0f, cycle_seconds=1, now=True)
        self.game.sound.play_music('music_starwars_theme', loops=-1)
        self.game.sound.play("sound_spin6")
        anim = dmd.Animation().load(dmd_path+'ufo.dmd')
        self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=8)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])

    def sw_outhole_active_for_500ms(self, sw):
        self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
        if self.game.switches.Reject.is_active():
            self.game.coils.Rejecthole_SunFlash.pulse(50)
            self.game.coils.Visormotor.enable()
        if self.game.switches.Leject.is_active():
            self.game.coils.Lejecthole_LeftPlFlash.pulse(50)
            self.game.coils.Visormotor.enable()

    def sw_slingL_active(self,sw):
        self.game.switchedCoils.acFlashPulse('RampRaise_LowPlFlash')
        self.game.sound.play("sound_slings")
        self.game.score(100)

    def sw_slingR_active(self,sw):
        self.game.sound.play("sound_slings")
        self.game.switchedCoils.acFlashPulse('RampRaise_LowPlFlash')
        self.game.score(100)


    def sw_vortex20k_active(self,sw):
        self.clear_layer()
        self.game.sound.play("sound_starwars_gun")
        self.game.score(2000)

    def sw_vortex100k_active(self,sw):
        self.clear_layer()
        self.game.sound.play("sound_starwars_schieten")
        self.game.score(10000)

    def sw_vortex5k_active(self,sw):
        self.clear_layer()
        if self.game.switches.vortex100k.time_since_change()>2 and self.game.switches.vortex20k.time_since_change()>2:
            self.game.sound.play("sound_stormtrooper_laser")
            self.game.score(500)


    def sw_advanceplanet_active(self,sw):
        anim = dmd.Animation().load(dmd_path+'saturnus.dmd')
        self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=6)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
    def sw_rampenter_active(self,sw):
        anim = dmd.Animation().load(dmd_path+'saturnusbmp.dmd')
        self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=8)
        self.animation_layer.composite_op = "blacksrc"
        self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])

    def sw_startButton_active_for_1s(self, sw):
        if self.game.switches.flipperLwR.is_active(1):
            self.game.effects.release_stuck_balls()
            self.game.coils.Ejecthole_LeftInsBFlash.pulse(30)
            print 'nu moet ejecthole gaan'
