# NO SNOOZE Alarm Clock v2
# Originally written on March 19, 2020
# Updated last on January 14, 2021 at 3:00 PM

import RPi.GPIO as GPIO
import time
import datetime
from lcd_display import lcd
import threading

# Day Constants #
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7) # Do not edit

#### ALARM CLOCK SETTINGS #####
SLEEP_IN_DAYS = [SUNDAY] # Days you don't want the alarm clock to go off
HOUR = 15 # Hour you want to wake up in 24hr military time. So for example, 6 AM = 6 and 6 PM = 18
MINUTES = 58 # Min you want to wake up at
###############################
# GPIO SETUP #
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)
################################
my_lcd = lcd()

def update_lcd():
    while True:
        my_lcd.lcd_display_string(time.strftime('%I:%M:%S %p'), 1)
        my_lcd.lcd_display_string(time.strftime('%a %b %d, 20%y'), 2)

if __name__ == '__main__':
    lcd_thread = threading.Thread(target=update_lcd,args=(),daemon=True).start()        
    # Execution loop
    while True:
        # Add something to occasionally display different LCD messages

        # Check if it's time to beep alarm.
        current_time_object = datetime.datetime.now()
        current_day, current_hour, current_minutes = current_time_object.weekday(), current_time_object.hour, current_time_object.minute
        
        if current_hour == HOUR and current_minutes == MINUTES and current_day not in SLEEP_IN_DAYS:
            for x in range(30):
                print('Wake up. NOW!')
                GPIO.output(BUZZER_PIN, GPIO.HIGH) # Beeeep 
                time.sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(1)
            