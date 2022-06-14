"""
Module for handling background threading operations
"""

import datetime
import subprocess
import threading
import time

import RPi.GPIO as GPIO

import button_actions
import config
import constants
from data_collection.weather import get_latest_forecast
from data_collection.sun import formatted_local_setrise

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class WeatherThread(threading.Thread):
    """ class for handling weather data updating """

    def __init__(self, data_lock):
        super().__init__(target=self.update_weather, args=(), daemon=True)
        self.data_lock = data_lock

    def update_weather(self):
        """ updates weather data  """

        while True:
            with self.data_lock:
                data = config.get_data_dictionary()
                data['forecast'] = get_latest_forecast()
                config.update_data_file(data)
            time.sleep(600) # wait ten minutes


class SunThread(threading.Thread):
    """ class for handling sunrise & sunset data updating """

    def __init__(self, data_lock):
        super().__init__(target=self.update_sun, args=(), daemon=True)
        self.data_lock = data_lock

    @staticmethod
    def seconds_to_midnight(date=None):
        """ returns seconds from current time to midnight """

        if date is None:
            date = datetime.datetime.now()
        return (datetime.datetime(year=date.year, month=date.month, day=date.day + 1) - date).seconds

    def update_sun(self):
        """ updates sunset / sunrise data """

        while True:
            with self.data_lock:
                data = config.get_data_dictionary()
                # later, fetch timezone from lat/long
                sunrise, sunset = formatted_local_setrise(constants.EST)
                data['sunset'] = sunset
                data['sunrise'] = sunrise
                config.update_data_file(data)
            # wait until next day (plus 10 seconds) to update
            time.sleep(SunThread.seconds_to_midnight() + 10)



class ButtonThread(threading.Thread):
    """ Thread for handling button presses """

    def __init__(self, button_action, pin, settings_lock):
        super().__init__(target=self.button_thread_function,
                         args=(), daemon=True)
        self.button_action = button_action
        self.pin = pin
        self.settings_lock = settings_lock

    def button_thread_function(self, delay=True):
        """ General function for executing button actions """

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        last_press_time = time.time()
        while True:
            if GPIO.input(self.pin) == GPIO.HIGH:
                if delay and time.time() - last_press_time < constants.CYCLE_BUTTON_DELAY:
                    continue
                last_press_time = time.time()
                self.button_action(self.settings_lock)


class BuzzerThread(threading.Thread):
    """ Thread for managing alarm clock buzzer sounds (and eventually mp3 sounds) """

    BUZZER_PIN = constants.BUZZER_PIN
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    def __init__(self):
        super().__init__(target=BuzzerThread.beeper, args=(), daemon=True)

    @staticmethod
    def play_sound():
        """ Plays piezoelectric buzzer to wake me up """

        settings = config.get_settings_dictionary()
        if settings['MP3_ENABLED']:
            # note: will allow more freedom to choose song later
            # for now it's hardcoded
            subprocess.run(['mpg123', 'music/chant.mp3'])

        for _ in range(10):
            GPIO.output(BuzzerThread.BUZZER_PIN, GPIO.HIGH)
            time.sleep(constants.TIME_BETWEEN_BEEPS)
            GPIO.output(BuzzerThread.BUZZER_PIN, GPIO.LOW)
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
            if BuzzerThread.is_time_to_play_sound():
                BuzzerThread.play_sound()


class ThreadManager:
    """ class for starting all background threads """
    def __init__(self):
        data_lock = threading.Lock()
        settings_lock = threading.Lock()
        self.threads = [
            WeatherThread(data_lock),
            SunThread(data_lock),
            ButtonThread(button_actions.cycle_bottom_lcd,
                         constants.CYCLE_BUTTON_PIN, settings_lock),
            BuzzerThread()
        ]

    def start_threads(self):
        """ starts all threads """

        for thread in self.threads:
            thread.start()
