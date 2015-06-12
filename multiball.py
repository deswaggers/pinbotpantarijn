import procgame
from procgame import *
import locale

# all paths
game_path = "C:\P-ROC\pyprocgame-master\games\VXtra_start/"
speech_path = game_path +"sound/speech/"
sound_path = game_path +"sound/fx/"
music_path = game_path +"sound/music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Multiball(game.Mode):
        def __init__(self, game, priority):
            super(Multiball, self).__init__(game, priority)

##            multi_anim = dmd.Animation().load(dmd_path+'mb_layer.dmd')
##            self.mb_layer = dmd.AnimatedLayer(frames=multi_anim.frames, opaque=False, repeat=True, hold=False, frame_time=2)
            self.score_layer = dmd.TextLayer(125, 6, self.game.fonts['num_14x10'], "right", opaque=False)
            self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False) #num_09Bx7 num_14x10
            self.value_layer = dmd.TextLayer(126, 22, self.game.fonts['tiny7'], "right", opaque=False) #07x5
##            self.text_layer1 = dmd.TextLayer(84, 8, self.game.fonts['07x5'], "center", opaque=False) #07x5
##            self.text_layer2 = dmd.TextLayer(84, 18, self.game.fonts['07x5'], "center", opaque=False) #07x5

            self.game.lampctrl.register_show('multiball_start', lampshow_path +"planeten_short.lampshow")
            self.game.lampctrl.register_show('visor_lampshow', lampshow_path +"Pinbot_1.lampshow")

            self.jackpot_value=100000
            self.multiball_score = 0
            self.multiball_status = 'restart_enabled'

        def mode_started(self):
            print("Debug, Multiball Mode Started")
            # start multiball intro
            self.multiball_intro()
            self.display_multiball_layer()
            self.game.sound.fadeout_music(time_ms=2800)

        def mode_stopped(self):
            print("Debug, Multiball Mode Stopped")

## lamps & animations

        def update_lamps(self):
            # stop current lightshow, start visor-lampshow
            self.game.lampctrl.stop_show()
            self.game.lampctrl.play_show('visor_lampshow', True, 'None')

            # Lampen voor jackpot
            self.game.effects.drive_lamp('eject1','fast')
            self.game.effects.drive_lamp('eject2','medium')
            self.game.effects.drive_lamp('eject3','slow')
            self.game.effects.drive_lamp('eject0','slow')
            self.game.effects.drive_lamp('score_energy','fast')
            self.game.effects.drive_lamp('solar_energy','medium')
            


##        def multiball_animation(self):
##             anim = dmd.Animation().load(dmd_path+"rk_mball_start.dmd")
##             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True,frame_time=4)
##             self.layer=self.animation_layer

        def jackpot_animation(self):
             self.cancel_delayed('display_multiball_layer')
             self.show_jackpot_value()
             anim = dmd.Animation().load(dmd_path+"jackpot.dmd")
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False,frame_time=4)
             self.animation_layer.add_frame_listener(-1, self.show_jackpot_value)
             self.animation_layer.add_frame_listener(-1, self.display_multiball_layer)
             self.layer=dmd.GroupedLayer(128,32,[self.animation_layer])

        def show_jackpot_value(self):
             self.value_layer.set_text("   JACKPOT: "+str(locale.format("%d", self.jackpot_value, True))+"   ")
             self.layer = self.value_layer

        def display_multiball_layer(self):
             p = self.game.current_player()
             scoreString = locale.format("%d",p.score, True)
             self.score_layer.set_text(scoreString,blink_frames=4)
             self.value_layer.set_text(" Jackpot: "+str(locale.format("%d", self.jackpot_value, True)))
##             self.layer = dmd.GroupedLayer(128, 32, [self.mb_layer, self.value_layer, self.score_layer])
             self.layer = dmd.GroupedLayer(128, 32, [self.value_layer, self.score_layer])
             self.delay(name='display_multiball_layer', event_type=None, delay=0.3, handler=self.display_multiball_layer)


        def totalscore_animation(self):
             self.total_score_layer.set_text(locale.format("%d", self.multiball_score, True))
             self.animation_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
             self.layer=dmd.GroupedLayer(128,32,[self.animation_layer, self.total_score_layer])

        def clear_layer(self):
            self.layer = None


## mode functions

        def multiball_intro(self):
            #self.game.sound.play()
            self.game.effects.gi_blinking(cycle_seconds=3)
            # Animation
##            self.multiball_animation()
            
            #play lightshow
            self.game.lampctrl.play_show('multiball_start', True, 'None')
            # delay multiballstart to wait for end of lampshow and perhaps animation
            self.delay(name='setup_multiball', event_type=None, delay=4, handler=self.setup_multiball)

        def setup_multiball(self):
             self.game.sound.play_music('music_mario_invincible')
             #stop lightshow
             self.game.lampctrl.stop_show()   
             
             #play music
##             self.game.sound.play_music()
             
             #update lamps for entire game after lampshow
             self.delay(name='update_lamps', event_type=None, delay=1, handler=self.update_lamps)

             # eject balls and close visor
             self.game.coils.Rejecthole_SunFlash.pulse(50)
             self.game.coils.Lejecthole_LeftPlFlash.pulse(50)
             self.delay(name='visor_closing' , event_type=None, delay=1, handler=self.close_visor)   

        def close_visor(self):
                self.game.visor_up_down.visor_move
                self.game.current_player().visor_lamps = [0,0,0,0,0]
                
        def end_multiball(self):
             self.game.sound.fadeout_music(time_ms=1500)
             
             self.cancel_delayed('display_multiball_layer')
             self.delay(name='stop_multiball', event_type=None, delay=2, handler=self.stop_multiball)
             self.jackpot_status=False
             self.totalscore_animation()
             print('number balls in play = ', self.game.trough.num_balls_in_play)
             self.game.effects.drive_lamp('eject1','off')
             self.game.effects.drive_lamp('eject2','off')
             self.game.effects.drive_lamp('eject3','off')
             self.game.effects.drive_lamp('eject0','off')
             self.game.effects.drive_lamp('score_energy','off')
             self.game.effects.drive_lamp('solar_energy','off')
             self.clear_layer()

        def stop_multiball(self):
             self.game.sound.play_music('music_starwars_theme')
             self.game.modes.remove(self)
##             self.callback('multiball')


        def score_jackpot(self):
            # play sound, animation and lightshow
##            self.game.sound.play()
##            self.jackpot_animation('jackpot')
            self.game.lampctrl.play_show('multiball_start', False, 'None')
            # calculate score
            self.game.effects.flashers_flash(time=2)
            self.game.score(self.jackpot_value)
            self.multiball_score += self.jackpot_value
            self.jackpot_animation()
            # update lamps after lightshow
            self.delay(name='update_lamps', event_type=None, delay=2, handler=self.update_lamps)



        def start_multiball(self):
             self.cancel_delayed('start_multiball')
             #self.game.effects.eject_ball(location='all')
             self.game.coils.Rejecthole_SunFlash.pulse(50)
             self.game.coils.Lejecthole_LeftPlFlash.pulse(50)
             self.display_multiball_layer()
             self.update_lamps()

        def bumper(self):
             self.jackpot_value+=200

## switches
        def sw_rampexit_active(self,sw):
             self.score_jackpot()
             return procgame.game.SwitchStop
        
        def sw_Leject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_Leject_active_for_600ms(self,sw):
             self.game.effects.eject_ball('Leject')
             self.score_jackpot()

        def sw_Reject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_Reject_active_for_600ms(self,sw):
             self.game.effects.eject_ball('Reject')
             self.score_jackpot()
             
        def sw_eject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_eject_active_for_600ms(self,sw):
             self.game.effects.eject_ball('eject')
             self.score_jackpot()



        def sw_Ubumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop    
        def sw_Lbumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop    
        def sw_Bbumper_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop




        # check whether allscoresdouble or end mode when a ball drains
        def sw_outhole_active(self,sw):
            print('number balls in play=', self.game.trough.num_balls_in_play)
            if self.game.trough.num_balls_in_play==2:
                self.game.coils.outhole_knocker.pulse(30)
                self.end_multiball()
                return procgame.game.SwitchStop
