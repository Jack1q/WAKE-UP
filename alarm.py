# NO SNOOZE Alarm Clock v2
# Originally written on March 19, 2020
# Updated last on January 14, 2021 at 3:00 PM

import RPi.GPIO as GPIO
import time
import datetime

# Day Constants #
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7) # Do not edit

#### ALARM CLOCK SETTINGS #####
SLEEP_IN_DAYS = [SATURDAY, SUNDAY] # Days you don't want the alarm clock to go off
HOUR = 6 # Hour you want to wake up in 24hr military time. So for example, 6 AM = 6 and 6 PM = 18
MINUTES = 30 # Min you want to wake up at
###############################
# GPIO SETUP #
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUZZER_PIN = 11
GPIO.setup(BUZZER_PIN, GPIO.OUT)
################################

# Execution loop
while True:
    current_time_object = datetime.datetime.now()
    current_day, current_hour, current_minutes = current_time_object.weekday(), current_time_object.hour, current_time_object.minute
    
    if current_hour == HOUR and current_minutes == MINUTES and current_day not in SLEEP_IN_DAYS:
        for x in range(30):
            print('Wake up. NOW!')
            GPIO.output(BUZZER_PIN, GPIO.HIGH) # Beeeep 
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)
            