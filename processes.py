import datetime
import multiprocessing
import time

import RPi.GPIO as GPIO

import config
from display.lcd_display import LCD
import messages


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class LCDProcess(multiprocessing.Process):
    
    lcd = LCD()
    lcd.backlight(0)
    
    def __init__(self):
        super().__init__(target=LCDProcess.update_lcd, args=(),daemon=True)
    
    @staticmethod
    def update_lcd():
        """ Constantly updates LCD screen with time and user's chosen data to track """
        
        DEFAULT_OPTION = 0
        while True:

            # Top LCD row:
            LCDProcess.lcd.lcd_display_string(messages.get_current_time(), 1)

            # Bottom LCD row:
            display_options = messages.get_display_options()
            try:
                selected_option = display_options[config.get_settings_dictionary()['DISPLAY_OPTION']]
            except ValueError:
                selected_option = display_options[DEFAULT_OPTION]
            LCDProcess.lcd.lcd_display_string(messages.formatter(selected_option()), 2)

class ButtonProcess(multiprocessing.Process):
        
    def __init__(self, button_action, pin):
        super().__init__(target=ButtonProcess.button_process_function, args=(button_action, pin), daemon=True)
    
    @staticmethod
    def button_process_function(button_action, pin, delay=True):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        last_press_time = time.time()
        while True:
            if GPIO.input(pin) == GPIO.HIGH:
                if delay and time.time() - last_press_time < 1:
                    continue
                last_press_time = time.time()
                button_action()
            
    
class ButtonActions:
    
    @staticmethod
    def cycle_bottom_lcd():
        settings = config.get_settings_dictionary()
        option = settings['DISPLAY_OPTION']
        if option >= len(messages.get_display_options()) - 1:
            option = 0
        else:
            option += 1
        settings['DISPLAY_OPTION'] = option
        config.update_settings_file(settings)
        

class BuzzerProcess(multiprocessing.Process):

    BUZZER_PIN = 23
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    def __init__(self):
        super().__init__(target=BuzzerProcess.beeper, args=(), daemon=True)
        
    @staticmethod
    def play_sound():
        """ Plays piezoelectric buzzer to wake me up """

        for _ in range(10):
            GPIO.output(BuzzerProcess.BUZZER_PIN, GPIO.HIGH)  
            time.sleep(1)
            GPIO.output(BuzzerProcess.BUZZER_PIN, GPIO.LOW)
            time.sleep(1)

    @staticmethod
    def is_time_to_play_sound():
        """ Checks if it is time to play a sound. """
        
        current_time_object = datetime.datetime.now()
        current_day, current_hour, current_minutes = current_time_object.weekday(), current_time_object.hour, current_time_object.minute
        settings = config.get_settings_dictionary()
        return current_hour == settings['HOUR'] and current_minutes == settings['MINUTES'] and current_day not in settings['SLEEP_IN_DAYS']

    @staticmethod
    def beeper():
        """
        Function for beep process: continously checks if it's time to beep,
        and does so if it is.
        """
        
        while True:
            if BuzzerProcess.is_time_to_play_sound():
                BuzzerProcess.play_sound()

    
