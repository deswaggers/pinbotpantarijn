# General play
# allerlei import: niet alles is nodig of wordt gebruikt: later op te schonen

#import random
import procgame
#import locale
#import logging
from os import listdir, walk
from os.path import join, splitext
#from time import time
#from random import randint
from procgame import *

# Dit importeert alle regels tijdens het gewone spel. Modes worden in ejectmodestart gestart.
from ejectmodestart import *
from bumpers import *
from visor import *
from droptargets import *
from ramp_multiball import *

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
        self.visor_rules = Visor(self.game, 11)
        self.droptarget_rules = Droptargets(self.game, 12)
        self.ramp_multiball = RampMultiball(self.game,13)


        self.game.current_player().mode_lamps = 0
        self.game.current_player().ramp_status_up = False

        ## variabelen die nodig zijn
        self.target_Energy_geraakt = False;


        ## Modestart straks naar elders, veel zaken in general_play nog op te schonen.
        #self.modes = [None, Mode1 (self.game, 19), Mode2 (self.game, 18), Mode3(self.game, 70)]
        #self.register_all_plugins()
        if self.game.sound.first_game_started ==False:
            self.register_all_sounds()
            self.game.lampctrl.register_show('rampenter_show', lampshow_path+"rampenter.lampshow")
            self.game.sound.first_game_started=True


        #self.musicjes = ['music_backtothefuture', 'music_doctorwho', 'music_galaxysong', 'music_hitchhiker',
        #                 'music_mario_invincible', 'music_interstellarcornfieldchase', 'music_starwars_theme',
        #                 'music_imperialmarch', 'music_starwars_cantina_band']
        self.musicjes = ["2018_overall_muziekje", "2018_fortnite_remix"]
       # ['2018_spacemusicnova', '2018_Starlight_achtergrondmuziekje',"2018_TheAlienWhistle_achtergrondmuziekje", "2018_CosmicMessages_achtergrondmuziekje", "2018_SpaceLoop_achtergrondmuziekje", "2018_whistlerbackgroundmusic", "2018_spacetrip", "2018_Pink-panther-theme"]

    def reset(self):
        pass

    def mode_started(self):
        # self.rampTimes = 1
        self.game.modes.add(self.ejectModestart_rules)

        self.game.modes.add(self.bumper_rules)
        self.game.modes.add(self.visor_rules)
        self.game.modes.add(self.droptarget_rules)

        if self.game.ball==1:
            self.game.animations.space_pinball_welcome()

        x = random.choice(self.musicjes)
        print x
        self.game.sound.play_music(x, loops=-1)
        #self.game.sound.play('speech_welcome')
        print "general play gestart"

        # Toegevoegd: visor altijd omhoog aan start bal als ie naar beneden is:
        # dit gaat botsen met visor-multiball, maar ik denk dat we het simpel moeten maken
        # en de regels zo moeten schrijven dat de visor alleen tijdens een bal omhoog kan,
        # en dat dan bij de volgende bal hij weer omhoog hoort. Anders wordt het ook
        # ingewikkeld met meerdere spelers
        if not self.game.switches.visorClosed.is_active():
            self.game.visor_up_down.visor_move()



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
        self.game.modes.remove(self.visor_rules)
        self.game.modes.remove(self.droptarget_rules)

        print 'generalplay stopped'

    def mode_tick(self):
        pass
        ## Afhankelijk van variabele per speler 'ramp_status_up' wordt de ramp omhoog of omlaat gebracht'


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
        #if self.game.current_player().mode_running:
        self.game.effects.drive_lamp('advance_planet','medium')
        #else:
        #    self.game.effects.drive_lamp('advance_planet','off')

    def reset_coils(self):
        self.game.effects.ramp_down()
        self.game.coils.Drops_RightInsBFlash.pulse(120)

## Switches regular gameplay
    def sw_shooterLane_open_for_100ms(self,sw):
        self.game.coils.RvisorGI.schedule(schedule=0x0f0f0f0f, cycle_seconds=1, now=True)
        self.game.coils.LvisorGI.schedule(schedule=0xf0f0f0f0, cycle_seconds=1, now=True)
        self.game.sound.play("speech_Cartoon-10")
        self.reset_coils()
        #self.game.animations.space_ship_flies()

    def sw_outhole_active_for_500ms(self, sw):
        self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
        self.game.current_player().mode_running = False
        if self.game.switches.Reject.is_active():
            self.game.coils.Rejecthole_SunFlash.pulse(50)
            self.game.coils.Visormotor.enable()
        if self.game.switches.Leject.is_active():
            self.game.coils.Lejecthole_LeftPlFlash.pulse(50)
            self.game.coils.Visormotor.enable()

    def sw_slingL_active(self,sw):
        self.game.coils.TopFlash3.pulse(45)
        self.game.coils.LvisorGI.pulse(40)
        self.game.sound.play("sound_slings")
        self.game.score(100)

    def sw_slingR_active(self,sw):
        self.game.coils.TopFlash4.pulse(45)
        self.game.coils.RvisorGI.pulse(40)
        self.game.sound.play("sound_slings")
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
        #self.game.animations.saturnus(score=1000)
        self.game.score(1000)
        self.game.sound.play("sound_cartoon_swirl")



    def sw_rampexit_active(self,sw):
        # willen we GI even laten knipperen? Lampje aanzetten? Hoe wordt die weer uit gezet?
        self.game.score(1000)
        self.game.effects.drive_lamp('score_energy','medium')
        self.game.effects.nonACFlashersFlash(2)
        if self.game.current_player().mode_running == False and self.target_Energy_geraakt==False:
            self.delay(name='Ramp_omlaag', event_type=None, delay=9, handler=self.ramp_up_finished)
            self.game.effects.ramp_up()


    def sw_scoreEnergy_active(self,sw):
        # punten? ramp naar beneden? met vertraging, of meteen en start multiball proberen?
        if (self.target_Energy_geraakt==False):
            print "Sw score energy geraakt"
            self.game.score(10000)
            self.game.effects.drive_lamp('score_energy','off')
            self.game.effects.ramp_down()
            self.game.modes.add(self.ramp_multiball)
            self.game.effects.nonACFlashersFlash(3)
            self.target_Energy_geraakt = True;


    def ramp_up_finished(self):
        self.game.effects.drive_lamp('score_energy','off')
        self.game.effects.ramp_down()




    def sw_Loutlane_active(self,sw):
        self.game.sound.play("sound_2018_Roblox_death_sound_effect")
        self.game.score(150)
        self.game.effects.nonACFlashersFlash(1)
    def sw_Routlane_active(self,sw):
        self.game.sound.play("sound_2018_Roblox_death_sound_effect")
        self.game.score(150)
        self.game.effects.nonACFlashersFlash(1)
    def sw_Linlane_active(self,sw):
        self.game.sound.play("sound_2017_lasershot")
        self.game.score(20)
    def sw_Rinlane_active(self,sw):
        self.game.sound.play("sound_2017_lasershot")
        self.game.score(20)



    def sw_startButton_active_for_1s(self, sw):
        if self.game.switches.flipperLwR.is_active(1):
            self.game.effects.release_stuck_balls()
            self.game.coils.Ejecthole_LeftInsBFlash.pulse(30)
            print 'nu moet ejecthole gaan'
