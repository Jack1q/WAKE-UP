""" Module for creating and managing Clock processes """

import datetime
import multiprocessing
import time

import RPi.GPIO as GPIO

import button_actions
import config
import constants
from display.lcd_display import LCD
import messages


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class LCDProcess(multiprocessing.Process):
    """ Process for manipulating and updating Clock screen with relevant data """

    lcd = LCD()
    lcd.backlight(constants.LCD_BACKLIGHT_STATE)

    def __init__(self):
        super().__init__(target=LCDProcess.update_lcd, args=(), daemon=True)

    @staticmethod
    def update_lcd():
        """ Constantly updates LCD screen with time and user's chosen data to track """

        while True:

            # Top LCD Line:
            LCDProcess.lcd.lcd_display_string(messages.get_current_time(), constants.LCD_TOP_LINE)

            # Bottom LCD Line:
            display_options = messages.get_display_options()
            try:
                settings = config.get_settings_dictionary()
                selected_option = display_options[settings['DISPLAY_OPTION']]
            except ValueError:
                selected_option = display_options[constants.DEFAULT_DISPLAY_OPTION]
            message = messages.fix_length(selected_option())
            LCDProcess.lcd.lcd_display_string(message, constants.LCD_BOTTOM_LINE)


class ButtonProcess(multiprocessing.Process):
    """ Process for handling button presses """

    def __init__(self, button_action, pin):
        super().__init__(target=ButtonProcess.button_process_function,
                         args=(button_action, pin), daemon=True)

    @staticmethod
    def button_process_function(button_action, pin, delay=True):
        """ General function for executing button actions """

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        last_press_time = time.time()
        while True:
            if GPIO.input(pin) == GPIO.HIGH:
                if delay and time.time() - last_press_time < constants.CYCLE_BUTTON_DELAY:
                    continue
                last_press_time = time.time()
                button_action()


class BuzzerProcess(multiprocessing.Process):
    """ Process for managing alarm clock buzzer sounds (and eventually mp3 sounds) """

    BUZZER_PIN = constants.BUZZER_PIN
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    def __init__(self):
        super().__init__(target=BuzzerProcess.beeper, args=(), daemon=True)

    @staticmethod
    def play_sound():
        """ Plays piezoelectric buzzer to wake me up """

        for _ in range(10):
            GPIO.output(BuzzerProcess.BUZZER_PIN, GPIO.HIGH)
            time.sleep(constants.TIME_BETWEEN_BEEPS)
            GPIO.output(BuzzerProcess.BUZZER_PIN, GPIO.LOW)
            time.sleep(constants.TIME_BETWEEN_BEEPS)

    @staticmethod
    def is_time_to_play_sound():
        """ Checks if it is time to play a sound. """

        current_datetime = datetime.datetime.now()
        day, hour, minutes = current_datetime.weekday(), \
                             current_datetime.hour, current_datetime.minute
        try:
            settings = config.get_settings_dictionary()
            return hour == settings['ALARM_HOUR'] and \
                minutes == settings['ALARM_MINUTES'] and \
                day not in settings['SLEEP_IN_DAYS']
        except ValueError:
            return False

    @staticmethod
    def beeper():
        """
        Function for beep process: continuously checks if it's time to beep,
        and does so if it is.
        """

        while True:
            if BuzzerProcess.is_time_to_play_sound():
                BuzzerProcess.play_sound()


class ProcessManager:
    """ Class for managing all Clock processes """

    def __init__(self):
        self.processes_in_use = [
            LCDProcess(),
            BuzzerProcess(),
            ButtonProcess(button_actions.cycle_bottom_lcd,
                          constants.CYCLE_BUTTON_PIN)
        ]

    def start_processes(self):
        """ Starts all processes in use """

        for process in self.processes_in_use:
            process.start()

    def terminate_processes(self):
        """ Terminates all processes in use """

        for process in self.processes_in_use:
            process.terminate()
