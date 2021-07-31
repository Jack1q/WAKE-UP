""" 
MyPiClock v0.4
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import RPi.GPIO as GPIO
import time
import datetime
from display.lcd_display import LCD
from config import get_settings_dictionary
from messages import get_display_options
import multiprocessing

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)

lcd = LCD()
lcd.backlight(0)

def update_lcd():
    """ Constantly updates LCD screen with time and user's chosen data to track """
    
    while True:

        # Top LCD row:
        lcd.lcd_display_string(messages.get_current_time(), 1)

        # Bottom LCD row:
        display_options = get_display_options()
        selected_option = display_options[get_settings_dictionary()['DISPLAY_OPTION']]
        lcd.lcd_display_string(selected_option(), 2)
        
def beep():
    """ Plays piezoelectric buzzer to wake me up """

    for x in range(30):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)

def is_time_to_beep():
    current_time_object = datetime.datetime.now()
    current_day, current_hour, current_minutes = current_time_object.weekday(), current_time_object.hour, current_time_object.minute
    settings = get_settings_dictionary()
    return current_hour == settings['HOUR'] and current_minutes == settings['MINUTES'] and current_day not in settings['SLEEP_IN_DAYS']

if __name__ == '__main__':
    lcd_process = multiprocessing.Process(target=update_lcd, args=(),daemon=True).start()
    while True:
        if is_time_to_beep():
           beep()