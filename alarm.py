# No-snooze Alarm Clock v2
# Originally written on March 19, 2020
# Updated on January 6, 2021 at 9:55 PM

import RPi.GPIO as GPIO
import time
import datetime

#### ALARM CLOCK SETTINGS #####
WEEKENDS_ON = False
SATURDAY = 5 # <-- Just made this to avoid using magic numbers in my code.
HOUR = 6
MINUTES = 30
##############################

# GPIO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)

while True:
    current_time_object = datetime.datetime.now()
    current_day = current_time_object.weekday()
    current_hour = current_time_object.hour
    current_minutes = current_time_object.minute

    if current_hour == HOUR and current_minutes == MINUTES and (WEEKENDS_ON or current_day < SATURDAY):
        for x in range(100):
            print('Wake up. NOW!')
            GPIO.output(BUZZER_PIN, GPIO.HIGH) # Beeeep 
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(1)

