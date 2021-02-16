""" 
MyPiClock v0.4
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on February 12, 2021 at 10:31 AM.
"""

# MyPiClock v0.4
# Smart LCD Alarm Clock with wake-up buzzer
# Originally written on March 19, 2020
# Updated last on February 9, 2021 at 4:37 PM

import RPi.GPIO as GPIO
import time
import datetime
from lcd_display import lcd
from config import *
from messages import *
import multiprocessing

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)

my_lcd = lcd()
my_lcd.backlight(0)

def update_lcd():
    """ 
    Constantly updates LCD screen with time and user's selected data 
    I am currently developing ways for the user to scroll through different
    datapoints rather than un-commenting to select a single one to use.
    """
    while True:
        # Top LCD row:
        my_lcd.lcd_display_string(time.strftime('%I:%M %p %m/%d'), 1)
        # Bottom LCD row:
        # my_lcd.lcd_display_string(get_current_date(), 2)
        # my_lcd.lcd_display_string(get_forecast(), 2)
        my_lcd.lcd_display_string(get_stock(STOCK_TICKER), 2)
        # my_lcd.lcd_display_string(get_unread(EMAIL_ADDRESS, EMAIL_PASSWORD), 2)
        # my_lcd.lcd_display_string(get_instagram_followers(INSTAGRAM_USERNAME))
        # my_lcd.lcd_display_string(CUSTOM_MESSAGE, 2)
        
def beep():
    """ Plays piezoelectric buzzer to wake me up """
    for x in range(30):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)

if __name__ == '__main__':
    lcd_process = multiprocessing.Process(target=update_lcd, args=(),daemon=True).start()
    while True:
        current_time_object = datetime.datetime.now()
        current_day, current_hour, current_minutes = current_time_object.weekday(), current_time_object.hour, current_time_object.minute
        if current_hour == HOUR and current_minutes == MINUTES and current_day not in SLEEP_IN_DAYS:
           beep()