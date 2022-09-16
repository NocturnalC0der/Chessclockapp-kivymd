from kivy.core.window import Window
from kivy.clock import Clock
import string
from time import strftime, strptime
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivymd.theming import ThemeManager


Clock.max_iteration = 150


# __version__ == '1.0'

class WindowManager(ScreenManager):
    pass
    
   

class ChessClockApp(MDApp):

    class TimeChangeWindow(Screen): 

        times_entered = False

        initial_time_top = ''
        initial_time_bottom = ''

        current_time_top = 0
        current_time_bottom = 0
        
        def change_time_top(self):
            time_top = self.ids.time_top.text
            digits = list(string.digits)
            if len(time_top) != 5:
                return 'invalid'
                
            else:
                if time_top[0] in digits and time_top[1] in digits and time_top[2] == ':' and time_top[3] in digits and time_top[4] in digits:
                    if int(time_top[3]) > 5:
                        return 'invalid'
                    else:
                        return time_top
                else:   
                    return 'invalid'

        def change_time_bottom(self):
            time_bottom = self.ids.time_bottom.text
            digits = list(string.digits)
            if len(time_bottom) != 5:
                return 'invalid'
            
            else: 
                if time_bottom[0] in digits and time_bottom[1] in digits and time_bottom[2] == ':' and time_bottom[3] in digits and time_bottom[4] in digits:
                    if int(time_bottom[3]) > 5:
                        return 'invalid'
                    else:
                        return time_bottom
                else: 
                    return 'invalid'


        def change_screen(self):
            self.manager.current = 'main_window'

        def change_times(self):
            ChessClockApp.MainWindow.set_times(ChessClockApp.MainWindow, self.change_time_top(), self.change_time_bottom())
            self.initial_time_top = self.change_time_top()
            self.initial_time_bottom = self.change_time_bottom()

        def check_times(self):
            
            if not self.times_entered:


                if self.change_time_bottom() == 'invalid' or self.change_time_top() == 'invalid':
                    self.ids.invalid_time_message.text = 'Invalid time(s), try again.'
                    self.ids.time_top.text = ''
                    self.ids.time_bottom.text = ''
                
                else:
                    
                    self.change_screen()
                    self.change_times()

                self.times_entered = True

            else:
                self.change_screen()
                if self.current_time_top == self.initial_time_top and self.current_time_bottom == self.initial_time_bottom:
                    self.change_times()

    class MainWindow(Screen):
        timer_started_bottom = False
        timer_started_top = False
        
        first_start_top = True
        first_start_bottom = True

        resume_bottom = False 
        resume_top = False

        end = False

        initial_time_top = ''
        initial_time_bottom = ''

        button_top = ObjectProperty()
        button_bottom = ObjectProperty()
        
        time_top = ''
        time_bottom = ''

        game_over = SoundLoader.load('time_out_beep.wav')

        def set_times(self, time_top, time_bottom, dt=0):
            if time_top =='invalid' or time_bottom == 'invalid':
                pass
            else:
                self.time_top = time_top
                self.time_bottom = time_bottom


        def initialize_times(self, time, initial_time, button, dt=0):
            if initial_time != time or button.text == '':
                button.text = time
                initial_time = time

        def on_enter(self):
            pass
            
            self.initialize_times(self.time_top, self.initial_time_top, self.button_top)
            self.initialize_times(self.time_bottom,  self.initial_time_bottom, self.button_bottom)

            self.pause_resume = self.ids.pause_resume_button
            self.reset_btn = self.ids.reset_button
            self.time_change_btn = self.ids.time_screen

        def start_countdown_top(self, dt):

            timer_seconds_top = int(self.button_top.text[3] + self.button_top.text[4])
            timer_minutes_top = int(self.button_top.text[0] + self.button_top.text[1])
            if self.timer_started_top:
                
                if timer_seconds_top == 00:
                    
                    if timer_seconds_top == 00 and timer_minutes_top == 00:
                        self.game_over.play()
                        self.timer_started_top = False
                        self.timer_started_bottom = False
                        self.end = True
                        Clock.unschedule(self.start_countdown_top, 1)
                        Clock.unschedule(self.start_countdown_bottom, 1)

                        
                        
                    else:
                        timer_minutes_top -= 1
                        timer_seconds_top = 59
                    
                else:
                    timer_seconds_top -= 1
                
                self.ids.button_top.text = f'{int(timer_minutes_top):02}:{int(timer_seconds_top):02}'


        def start_countdown_bottom(self, dt):        
            timer_seconds_bottom = int(self.button_bottom.text[3] + self.button_bottom.text[4])        
            timer_minutes_bottom = int(self.button_bottom.text[0] + self.button_bottom.text[1])
            
            if self.timer_started_bottom:

                if timer_seconds_bottom == 00:

                    if timer_seconds_bottom == 00 and timer_minutes_bottom == 00:
                        self.game_over.play()
                        self.timer_started_top = False
                        self.timer_started_bottom = False
                        self.end = True
                        Clock.unschedule(self.start_countdown_bottom, 1)
                        Clock.unschedule(self.start_countdown_top, 1)
                        
                    
                    else:
                        timer_minutes_bottom -= 1
                        timer_seconds_bottom = 59
                
                else:
                    timer_seconds_bottom -= 1    
                self.ids.button_bottom.text = f'{int(timer_minutes_bottom):02}:{int(timer_seconds_bottom):02}'


        def switch_time_top(self):
            if self.timer_started_top == False and self.timer_started_bottom == True or self.pause_resume.icon == 'play' or self.button_top == '00:00' or self.end == True:    
                pass
            else: 
                Clock.unschedule(self.start_countdown_top)
                self.ids.time_screen.disabled = True
                self.pause_resume.disabled = False

            
                if self.timer_started_top == False and self.timer_started_bottom == False:
                    self.timer_started_bottom = True
                    self.first_start_bottom = False
                    Clock.schedule_interval(self.start_countdown_bottom, 1)
                
                
                
                elif self.timer_started_top == True and self.timer_started_bottom == False:
                    self.timer_started_top = not self.timer_started_top                    
                    self.timer_started_bottom = not self.timer_started_bottom
                    self.first_start_bottom = False
                    Clock.schedule_interval(self.start_countdown_bottom, 1)

                
                else:
                    self.timer_started_top = not self.timer_started_top
                    
                
                    self.timer_started_bottom = not self.timer_started_bottom
                
                self.initial_time_bottom = self.time_bottom
                self.ids.button_top.disabled = True
                self.ids.button_bottom.disabled = False

        def switch_time_bottom(self):
            if self.timer_started_bottom == False and self.timer_started_top == True or self.pause_resume.icon == 'play' or self.button_bottom == '00:00' or self.end == True:
                pass            
            
            else: 
                Clock.unschedule(self.start_countdown_bottom)
                self.ids.time_screen.disabled = True
                self.pause_resume.disabled = False
                if self.timer_started_top == False and self.timer_started_bottom == False:
                    self.timer_started_top = True
                    self.first_start_top = False
                    Clock.schedule_interval(self.start_countdown_top, 1)            
                
                elif self.timer_started_bottom == True and self.timer_started_top == False:
                    self.timer_started_bottom = not self.timer_started_bottom                    
                    self.timer_started_top = not self.timer_started_top
                    self.first_start_top = False
                    Clock.schedule_interval(self.start_countdown_top, 1)
                
                else:

                    self.timer_started_bottom = not self.timer_started_bottom
                    
                    self.timer_started_top = not self.timer_started_top
            
                
                self.initial_time_top = self.time_top
                self.ids.button_top.disabled = False
                self.ids.button_bottom.disabled = True


        def pause_func(self):
            
            if self.timer_started_top:
                self.resume_top = True
                self.timer_started_top = False
            
            if self.timer_started_bottom: 
                self.resume_bottom = True
                self.timer_started_bottom = False


            self.pause_resume.icon = 'play'
            self.ids.time_screen.disabled = False
            self.reset_btn.disabled = False

                
        def resume(self):
            self.pause_resume.icon = 'pause'
            if self.resume_top:
                self.timer_started_top = True
                self.resume_top = False
            
            if self.resume_bottom:
                self.timer_started_bottom = True
                self.resume_bottom = False

            self.ids.time_screen.disabled = True
            self.reset_btn.disabled = True
            
        def pause_resume_func(self):
            if self.pause_resume.icon == 'pause' and self.pause_resume.disabled == False:
                self.pause_func()
                return 'pause resume test'
                
            elif self.pause_resume.icon == 'play'and self.pause_resume.disabled == False:
                self.resume()
                return 'pause resume test 2'
                
        def reset(self):
            if self.pause_resume.icon == 'play' or self.button_top == '00:00' or self.button_bottom == '00:00': 
                self.button_top.text = self.initial_time_top
                self.button_bottom.text = self.initial_time_bottom
                
                self.timer_started_top = False
                self.timer_started_bottom = False
                self.first_start_bottom = True
                self.first_start_top = True
                Clock.unschedule(self.start_countdown_top, 1)
                Clock.unschedule(self.start_countdown_bottom, 1)
                self.button_top.disabled = False
                self.button_bottom.disabled = False
                self.reset_btn.disabled = True
                self.pause_resume.disabled = True
                self.pause_resume.icon = 'pause'
                ChessClockApp().TimeChangeWindow().times_entered = False


    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = 'Light'
        sm = ScreenManager()
    
        sm.add_widget(self.TimeChangeWindow(name='time_change_window'))
        sm.add_widget(self.MainWindow(name='main_window'))

if __name__ == '__main__':
    ChessClockApp().run()

