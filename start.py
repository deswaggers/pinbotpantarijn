import sys
sys.path.append(sys.path[0]+'/../..') # Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.
import procgame
import pinproc
from switchedcoils import *
from effects import *
from general_play import *
from match import *
from visor_up_down import *
from procgame import *
from threading import Thread
from random import *
from time import strftime
import string
import time
import locale
import math
import copy
import yaml
import random
import logging
import Image


logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#game_locale = config.value_for_key_path('std_locale')
#locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # used to put commas in the score.
#NOTE: not needed on raspi

game_path = "/home/pi/VXtra_start/"
print("Using game_path at: %s "%(game_path))
logging.info("Game Path is: "+game_path)


fonts_path = game_path + "dmd/fonts/"
shared_sound_path = game_path + "sound/service/"

machine_config_path = game_path + "config/Pinbot.yaml"
settings_path = game_path +"config/settings.yaml"
game_data_path = game_path +"config/game_data.yaml"
game_data_template_path = game_path +"config/game_data_template.yaml"
settings_template_path = game_path +"config/settings_template.yaml"

speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
lampshow_path = game_path +"lampshows/"
font_tiny7 = dmd.Font(fonts_path+"04B-03-7px.dmd")
font_jazz18 = dmd.Font(fonts_path+"Jazz18-18px.dmd")
font_14x10 = dmd.Font(fonts_path+"Font14x10.dmd")
font_18x12 = dmd.Font(fonts_path+"Font18x12.dmd")
font_07x4 = dmd.Font(fonts_path+"Font07x4.dmd")
font_07x5 = dmd.Font(fonts_path+"Font07x5.dmd")
font_09Bx7 = dmd.Font(fonts_path+"Font09Bx7.dmd")

lampshow_files = [lampshow_path +"Pinbot_1.lampshow", \
                  lampshow_path +"Pinbot_1.lampshow", ]


class Attract(game.Mode):
    """docstring for AttractMode"""
    def __init__(self, game):
        super(Attract, self).__init__(game, 1)
        self.log = logging.getLogger('rk.attract')
        self.display_order = [0,1,2,3,4,5,6,7,8,9]
        self.display_index = 0
        self.player_layers = []
        #Disable flippers
        self.game.coils.flipperEnable.disable()

    def mode_topmost(self):
        pass

    def mode_started(self):

                # run feature lamp patterns
                self.change_lampshow()

                #check for stuck balls
                self.delay(name='stuck_balls', event_type=None, delay=1, handler=self.game.effects.release_stuck_balls)

                print("Trough is full:" +str(self.game.trough.is_full()))

                #create dmd attract screens
                self.williams_logo = dmd.AnimatedLayer(frames=dmd.Animation().load(game_path+'dmd/williams_animated.dmd').frames,frame_time=1,hold=True)

                self.proc_logo = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(game_path+'dmd/Splash.dmd').frames[0])
                self.proc_logo.transition = dmd.ExpandTransition(direction='vertical')

                self.press_start = dmd.TextLayer(128/2, 18, font_09Bx7, "center", opaque=True).set_text("PRESS START", seconds=None, blink_frames=1)
                self.free_play = dmd.TextLayer(128/2, 6, font_09Bx7, "center", opaque=False).set_text("FREE PLAY")
                self.coins_layer = dmd.GroupedLayer(128, 32, [self.free_play, self.press_start])
                self.coins_layer.transition = dmd.PushTransition(direction='north')

                self.p1_layer = dmd.TextLayer(0, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.p2_layer = dmd.TextLayer(128, 0, self.game.fonts['num_09Bx7'], "right", opaque=False)
                self.p3_layer = dmd.TextLayer(0, 24, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.p4_layer = dmd.TextLayer(128, 24, self.game.fonts['num_09Bx7'], "right", opaque=False)
                self.last_scores_layer = dmd.GroupedLayer(128, 32, [self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer])
                self.last_scores_layer.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.game_over_layer = dmd.TextLayer(128/2, 10, font_09Bx7, "center", opaque=True).set_text("GAME OVER")
                self.game_over_layer.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.scores_layer = dmd.TextLayer(128/2, 11, font_09Bx7, "center", opaque=True).set_text("HIGH SCORES")
                self.scores_layer.transition = dmd.PushTransition(direction='west')

                gen = dmd.MarkupFrameGenerator()
                credits_frame = gen.frame_for_markup("""

#CREDITS#
[VWOxtra:]
[Tein]
[Mees]
[Sypke]
[Ket]
[Alvin]
[Corijn]
[Teun]
[Tibi]

[Begeleiding:]
[Jelle Besseling]
[Steven van der Staaij]

[Rules and software: ]

[]
[Dots & Animations: ]

[]
[Lightshows: ]

[]
[Music & SFX: ]

[]
[Graphic design:]

[]
[Hardware mods:]

""")

                self.credits_layer = dmd.PanningLayer(width=128, height=32, frame=credits_frame, origin=(0,0), translate=(0,1), bounce=False)

                #run attract dmd screens
                self.attract_display()


    def sw_outhole_active(self, sw):
            self.game.switchedCoils.acCoilPulse('outhole_knocker',45)
            return True


    def change_lampshow(self):
            shuffle(self.game.lampshow_keys)
            self.game.lampctrl.play_show(self.game.lampshow_keys[0], repeat=True)
            self.delay(name='lampshow', event_type=None, delay=10, handler=self.change_lampshow)


    def attract_display(self):
            script = list()

            script.append({'seconds':2.0, 'layer':self.proc_logo})
            script.append({'seconds':7.0, 'layer':self.williams_logo})
            script.append({'seconds':3.0, 'layer':self.coins_layer})
            script.append({'seconds':20.0, 'layer':self.credits_layer})
            script.append({'seconds':3.0, 'layer':self.scores_layer})

            for frame in highscore.generate_highscore_frames(self.game.highscore_categories):
                new_layer = dmd.FrameLayer(frame=frame)
                new_layer.transition = dmd.PushTransition(direction='west')
                script.append({'seconds':2.0, 'layer':new_layer})

            #add in the game over screen
            go_index=3
            go_time=3
            if self.game.system_status=='game_over':
                go_index=0
                go_time=3

                #add in the player scores after a game is played
                self.player_layers=[self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer]
                for i in range(len(self.game.players)):
                     score = self.game.players[i].score
                     #digit = str(score)
                     self.player_layers[i].set_text(locale.format("%d", score, True))

                ls_index=0
                ls_time=10
                self.game.system_status='attract'
                print("system status = "+self.game.system_status.upper())

                script.insert(ls_index,{'seconds':ls_time, 'layer':self.last_scores_layer})

            script.insert(go_index,{'seconds':go_time, 'layer':self.game_over_layer})

            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)


    def mode_stopped(self):
        self.game.lampctrl.stop_show()

    def mode_tick(self):
        pass

    # Enter service mode when the enter button is pushed.
    def sw_enter_active(self, sw):
        for lamp in self.game.lamps:
            lamp.disable()
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_exit_active(self, sw):
        return True

    # Outside of the service mode, up/down control audio volume.
    def sw_down_active(self, sw):
        volume = self.game.sound.volume_down()
        self.game.set_status("Volume Down : " + str(volume))
        return True

    def sw_up_active(self, sw):
        volume = self.game.sound.volume_up()
        self.game.set_status("Volume Up : " + str(volume))
        return True

    # Start button starts a game if the trough is full.  Otherwise it
    # initiates a ball search.
    def sw_startButton_active(self, sw):
        if self.game.trough.is_full:
            # Remove attract mode from mode queue - Necessary?
            self.game.modes.remove(self)
            # Initialize game
            self.game.start_game()
            # Add the first player
            self.game.add_player()
            # Start the ball.  This includes ejecting a ball from the trough.
            self.game.start_ball()
            #SYS11: enable the flippers
            self.game.coils.flipperEnable.enable()
        else:
            self.game.set_status("Ball Search!")
            self.game.effects.ball_search()
        return True


class BaseGameMode(game.Mode):
    """docstring for BaseGameMode"""
    def __init__(self, game):
                super(BaseGameMode, self).__init__(game, 2)
                self.tilt_layer = dmd.TextLayer(128/2, 7, font_18x12, "center", opaque=True).set_text("TILT")
                self.layer = None # Presently used for tilt layer
                self.ball_starting = True

                #register speech call files
                self.game.sound.register_sound('tilt_warning', speech_path+"tilt_warning.ogg")
                self.game.sound.register_sound('tilt_', sound_path+"tilt.ogg")
                #register sound effects files
                self.game.sound.register_sound('ball_saved', speech_path+"ball_saved.aiff")
                #self.game.sound.register_sound('shooterlane', sound_path+"motor_driveaway.aiff")
                #self.game.sound.register_music('shooterlane_loop', music_path+"shooterlane_loop.ogg")

                self.ball_saved = False
                self.ball_save_time = self.game.user_settings['Gameplay (Feature)']['Ballsave Timer']
                self.instant_info_on = False

    def mode_started(self):
        #debug
        print("Basic Game Mode Started, Ball "+str(self.game.ball))
        #set player status
        self.game.set_player_stats('status','general')

        #Disable any previously active lamp
        for lamp in self.game.lamps:
            lamp.disable()


        # Enable the flippers
        self.game.coils.flipperEnable.enable()

        # Each time this mode is added to game Q, set this flag true.
        self.ball_starting = True

        # Reset skillshot flag
        self.skillshot_active = False

        #setup basic modes
        self.add_basic_modes(self);

        #Update lamp status's for all modes
        self.game.update_lamps()

        # Put the ball into play and start tracking it.
        self.game.trough.launch_balls(1, self.ball_launch_callback)

        #Not SYS11: Enable ball search in case a ball gets stuck during gameplay.
        #self.game.ball_search.enable()

        # Reset tilt warnings and status
        self.times_warned = 0;
        self.tilt_status = 0

        # In case a higher priority mode doesn't install it's own ball_drained
        # handler.
        self.game.trough.drain_callback = self.ball_drained_callback

        #ball save callback - exp
        self.game.ball_save.callback = self.ball_save_callback

    def add_basic_modes(self,ball_in_play):

            #lower priority basic modes
            self.generalplay = Generalplay(self.game, 20)

            #start modes
            self.game.modes.add(self.generalplay)


    def ball_save_callback(self):
            anim = dmd.Animation().load(game_path+"dmd/ball_saved.dmd")
            self.layer = dmd.AnimatedLayer(frames=anim.frames,hold=False)
            self.game.sound.play_voice('ball_saved')
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear)
            self.ball_saved = True

    def clear(self):
            self.layer=None

    def ball_launch_callback(self):
            #print("Debug - Ball Starting var is:"+str(self.ball_starting))
            if self.ball_starting:
                self.game.ball_save.start_lamp()
                #start background music
                #self.game.effects.rk_play_music()
                pass

    def mode_tick(self):
            if self.game.switches.startButton.is_active(1) and self.game.switches.flipperLwL.is_active(1) and self.game.switches.flipperLwR.is_active():
                print("reset button code entered")
                self.game.sound.stop_music()
                self.game.end_run_loop()

                while len(self.game.dmd.frame_handlers) > 0:
                    del self.game.dmd.frame_handlers[0]

                del self.game.proc

    def mode_stopped(self):
            print("Basic Game Mode Ended, Ball "+str(self.game.ball))

            # Ensure flippers are disabled
            self.game.coils.flipperEnable.disable()

            self.game.modes.remove(self.generalplay)


    def ball_drained_callback(self):
        if self.game.trough.num_balls_in_play == 0:
            # End the ball
            self.finish_ball()

    def finish_ball(self):
        #music fadeout
        self.game.sound.fadeout_music()

        # Turn off tilt display (if it was on) now that the ball has drained.
        if self.tilt_status and self.layer == self.tilt_layer:
            self.layer = None


        # Create the bonus mode so bonus can be calculated.
        #self.bonus = Bonus(self.game, 98)
        #self.game.modes.add(self.bonus)

        # Only compute bonus if it wasn't tilted away.
        #if not self.tilt_status:
        #    self.bonus.calculate(self.end_ball)
        #else:
        self.end_ball()

    def end_ball(self):
        #remove bonus mode
        #self.game.modes.remove(self.bonus)

        # Tell the game object it can process the end of ball
        # (to end player's turn or shoot again)
        self.game.end_ball()


    def sw_startButton_active(self, sw):
        if self.game.ball == 1 and len(self.game.players)<self.game.max_players:
            p = self.game.add_player()
            self.game.set_status(p.name + " added")

    def sw_startButton_active_for_2s(self, sw):
        if self.game.ball > 1 and self.game.user_settings['Machine (Standard)']['Game Restart']:
            self.game.set_status("Reset!")

            # Need to build a mechanism to reset AND restart the game.  If one ball
            # is already in play, the game can restart without plunging another ball.
            # It would skip the skill shot too (if one exists).

            # Currently just reset the game.  This forces the ball(s) to drain and
            # the game goes to AttractMode.  This makes it painfully slow to restart,
            # but it's better than nothing.
            self.game.reset()
            return True

    def sw_shooterLane_open_for_1s(self,sw):
        if self.ball_starting:
            self.ball_starting = False
            #ball_save_time = 10 VIA MENU
            self.game.ball_save.start(num_balls_to_save=1, time=self.ball_save_time, now=True, allow_multiple_saves=False)




    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_tilt_active(self, sw):
        if self.times_warned == self.game.user_settings['Machine (Standard)']['Tilt Warnings']:
            self.tilt()
        else:
            self.times_warned += 1
            #play sound
            self.game.sound.play_voice('tilt_warning')
            #add a display layer and add a delayed removal of it.
            self.game.set_status("Tilt Warning " + str(self.times_warned) + "!")

    def tilt(self):
        # Process tilt.
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.tilt_status == 0:

            #play sound
            self.game.sound.play('tilt_')
            self.game.sound.stop_music()

            # Display the tilt graphic
            self.layer = self.tilt_layer

            # Disable flippers so the ball will drain.
            self.game.coils.flipperEnable.disable()

            # Make sure ball won't be saved when it drains.
            self.game.ball_save.disable()
            #self.game.modes.remove(self.ball_save)

            # Make sure the ball search won't run while ball is draining.
            #NOT SYS11: self.game.ball_search.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            # Kick balls out of places it could be stuck.
            self.game.effects.release_stuck_balls()

            self.tilt_status = 1



class Game(game.BasicGame):
    """docstring for Game"""
    def __init__(self, machine_type):
        super(Game, self).__init__(machine_type)
        self.sound = procgame.sound.SoundController(self)
        self.lampctrl = procgame.lamps.LampController(self)
        self.settings = {}

    def save_settings(self):
        #self.write_settings(settings_path)
        super(Game, self).save_settings(settings_path)

    def save_game_data(self):
        super(Game, self).save_game_data(game_data_path)

    def create_player(self, name):
        return rkPlayer(name)


    def setup(self):
        """docstring for setup"""
        self.load_config(self.yamlpath)

        self.load_settings(settings_template_path, settings_path)
        self.sound.music_volume_offset = self.user_settings['Sound']['Music volume offset']
        self.sound.set_volume(self.user_settings['Sound']['Initial volume'])
        self.load_game_data(game_data_template_path, game_data_path)

        #define system status var
        self.system_status='power_up'
        print("system status = "+self.system_status.upper())


        print("Initial switch states:")
        for sw in self.switches:
            print("  %s:\t%s" % (sw.name, sw.state_str()))

        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']
        self.score_display.set_left_players_justify(self.user_settings['Display']['Left side score justify'])

        # Note - Game specific item:
        # The last parameter should be the name of the game's ball save lamp
        self.ball_save = procgame.modes.BallSave(self, self.lamps.shootAgain, 'shooterLane')

        trough_switchnames = []
        # Note - Game specific item:
        # This range should include the number of trough switches for
        # the specific game being run.  In range(1,x), x = last number + 1.
        for i in range(1,4):
            trough_switchnames.append('trough' + str(i))
        early_save_switchnames = ['Routlane','Loutlane']

        # Note - Game specific item:
        # Here, trough6 is used for the 'eject_switchname'.  This must
        # be the switch of the next ball to be ejected.  Some games
        # number the trough switches in the opposite order; so trough1
        # might be the proper switchname to user here.
        self.trough = procgame.modes.Trough(self,trough_switchnames,'trough3','trough', early_save_switchnames, 'shooterLane', self.drain_callback)

        # Link ball_save to trough
        self.trough.ball_save_callback = self.ball_save.launch_callback
        self.trough.num_balls_to_save = self.ball_save.get_num_balls_to_save
        self.ball_save.trough_enable_ball_save = self.trough.enable_ball_save

        # Setup and instantiate service mode
        self.sound.register_sound('service_enter', shared_sound_path+"sfx-menu-enter.wav")
        self.sound.register_sound('service_exit', shared_sound_path+"sfx-menu-exit.wav")
        self.sound.register_sound('service_next', shared_sound_path+"sfx-menu-up.wav")
        self.sound.register_sound('service_previous', shared_sound_path+"sfx-menu-down.wav")
        self.sound.register_sound('service_switch_edge', shared_sound_path+"sfx-menu-switch-edge.wav")
        self.sound.register_sound('service_save', shared_sound_path+"sfx-menu-save.wav")
        self.sound.register_sound('service_cancel', shared_sound_path+"sfx-menu-cancel.wav")
        self.service_mode = procgame.service.ServiceMode(self,100,font_tiny7,[])

        # Highscore sound
        self.sound.register_sound('high score', speech_path+'bk2k_champion.wav')

        # Setup fonts
        self.fonts = {}
        self.fonts['tiny7'] = font_tiny7
        self.fonts['jazz18'] = font_jazz18
        self.fonts['18x12'] = font_18x12
        self.fonts['07x5'] = font_07x5
        self.fonts['num_14x10'] = font_14x10
        self.fonts['num_07x4'] = font_07x4
        self.fonts['num_09Bx7'] = font_09Bx7

        #setup paths
        self.paths = {}
        self.paths['game'] = game_path
        self.paths['sound'] = sound_path
        self.paths['speech'] = speech_path
        self.paths['music'] = music_path

        # Register lampshow files for attract
        self.lampshow_keys = []
        key_ctr = 0
        for file in lampshow_files:
            #if file.find('flasher',0)>0:
            #    key = 'attract_flashers_' + str(key_ctr)
            #else:
            key = 'attract_lamps_' + str(key_ctr)
            self.lampshow_keys.append(key)
            self.lampctrl.register_show(key, file)
            key_ctr += 1

        # Setup High Scores
        self.highscore_categories = []

        # Classic High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
        self.highscore_categories.append(cat)


        for category in self.highscore_categories:
            category.load_from_game(self)


        #Maximum Players
        self.max_players = 4;

        #add basic modes
        #------------------
        #attract mode
        self.attract_mode = Attract(self)
        #basic game control mode
        self.base_game_mode = BaseGameMode(self)
        #ac_select
        self.switchedCoils = SwitchedCoils(self,4)
        #effects mode
        self.effects = Effects(self)
        #match mode
        self.match = Match(self,10)
        #updown ding
        self.visor_up_down = Visor_up_down(self, 10)
        #------------------


        # Instead of resetting everything here as well as when a user initiated reset occurs,
        # do everything in self.reset() and call it now and during a user initiated reset.
        self.reset()

    def set_player_stats(self,id,value):
        p = self.current_player()
        p.player_stats[id]=value

    def get_player_stats(self,id):
        p = self.current_player()
        return p.player_stats[id]

    def add_player_stats(self,id,value):
        p = self.current_player()
        p.player_stats[id]+=value

    def reset(self):
        # Reset the entire game framework
        super(Game, self).reset()

        # Add the basic modes to the mode queue
        self.modes.add(self.attract_mode)
        #Not SYS11: self.modes.add(self.ball_search)
        self.modes.add(self.ball_save)
        self.modes.add(self.trough)
        self.modes.add(self.effects)


    # Empty callback just incase a ball drains into the trough before another
    # drain_callback can be installed by a gameplay mode.
    def drain_callback(self):
        pass

    def start_game(self):
        super(Game, self).start_game()
        self.game_data['Audits']['Games Started'] += 1
        self.system_status='game_started'
        print("system status = "+self.system_status.upper())

    def ball_starting(self):
        super(Game, self).ball_starting()
        self.modes.add(self.base_game_mode)

    def ball_ended(self):
        self.modes.remove(self.base_game_mode)
        super(Game, self).ball_ended()
        # Handle stats for ball here
        #ball_time = self.get_ball_time()
        self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        self.game_data['Audits']['Balls Played'] += 1
        print("balls played, ball ended")

    def game_ended(self):
        super(Game, self).game_ended()
        self.modes.remove(self.base_game_mode)



        # High Score Stuff
        seq_manager = highscore.EntrySequenceManager(game=self, priority=2)
        seq_manager.finished_handler = self.highscore_entry_finished
        seq_manager.logic = highscore.CategoryLogic(game=self, categories=self.highscore_categories)
        seq_manager.ready_handler = self.highscore_entry_ready_to_prompt
        self.modes.add(seq_manager)

    def highscore_entry_ready_to_prompt(self, mode, prompt):
        self.sound.play_voice('high score')
        self.effects.flippers(True)
        banner_mode = game.Mode(game=self, priority=8)
        markup = dmd.MarkupFrameGenerator()
        markup.font_plain = dmd.font_named('04B-03-7px.dmd')
        markup.font_bold = dmd.font_named('04B-03-7px.dmd')
        text = '\n[GREAT JOB]\n#%s#\n' % (prompt.left.upper()) # we know that the left is the player name
        frame = markup.frame_for_markup(markup=text, y_offset=0)
        banner_mode.layer = dmd.ScriptedLayer(width=128, height=32, script=[{'seconds':4.0, 'layer':dmd.FrameLayer(frame=frame)}])
        banner_mode.layer.on_complete = lambda: self.highscore_banner_complete(banner_mode=banner_mode, highscore_entry_mode=mode)
        self.modes.add(banner_mode)

    def highscore_banner_complete(self, banner_mode, highscore_entry_mode):
        self.modes.remove(banner_mode)
        highscore_entry_mode.prompt()

    def highscore_entry_finished(self, mode):
        self.modes.remove(mode)
        self.effects.flippers(False)
        self.modes.add(self.match)

        # Handle stats for last ball here
        #self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        #self.game_data['Audits']['Balls Played'] += 1
        print("game time : highscore_entry")

        # Handle game stats here
        for i in range(0,len(self.players)):
            game_time = self.get_game_time(i)
            self.game_data['Audits']['Avg Game Time'] = self.calc_time_average_string( self.game_data['Audits']['Games Played'], self.game_data['Audits']['Avg Game Time'], game_time)
            self.game_data['Audits']['Games Played'] += 1

        for i in range(0,len(self.players)):
            self.game_data['Audits']['Avg Score'] = self.calc_number_average(self.game_data['Audits']['Games Played'], self.game_data['Audits']['Avg Score'], self.players[i].score)
        self.save_game_data()

    def calc_time_average_string(self, prev_total, prev_x, new_value):
          prev_time_list = prev_x.split(':')
          prev_time = (int(prev_time_list[0]) * 60) + int(prev_time_list[1])
          avg_game_time = int((int(prev_total) * int(prev_time)) + int(new_value)) / (int(prev_total) + 1)
          avg_game_time_min = avg_game_time/60
          avg_game_time_sec = str(avg_game_time%60)
          if len(avg_game_time_sec) == 1:
                  avg_game_time_sec = '0' + avg_game_time_sec
          return_str = str(avg_game_time_min) + ':' + avg_game_time_sec
          return return_str

    def calc_number_average(self, prev_total, prev_x, new_value):
          avg_game_time = int((prev_total * prev_x) + new_value) / (prev_total + 1)
          return int(avg_game_time)

    def set_status(self, text):
        self.dmd.set_message(text, 3)
        print(text)

    def extra_ball_count(self):
        p = self.current_player()
        p.extra_balls += 1


class rkPlayer(game.Player):

    def __init__(self, name):
                super(rkPlayer, self).__init__(name)

                self.player_stats = {}
                self.player_stats['status']=''
                self.visor_position='up'
                self.visor_lamps = [0,0,0,0,0]
                self.visor_balls = 0
                self.mode_running = False
                self.mode_listener = None
                self.eject_mode_object = None
                self.eject_mode_modes = []
                self.eject_mode_played_modes = []

    def set_mode_running(self, mode_running):
        self.mode_running = mode_running
        if self.eject_mode_object is not None:
            self.eject_mode_object.mode_running_changed(mode_running)


def main():

    config = yaml.load(open(machine_config_path, 'r'))
    print("Using config at: %s "%(machine_config_path))
    machine_type = config['PRGame']['machineType']
    config = 0
    game = None
    try:
        game = Game(machine_type)
        game.yamlpath = machine_config_path
        game.setup()
        game.run_loop()

    finally:
        del game


if __name__ == '__main__': main()
