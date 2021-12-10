""" Mostly hardware-related constants """

# CHANGE IF YOU WANT
BUZZER_PIN = 23
CYCLE_BUTTON_PIN = 10
CYCLE_BUTTON_DELAY = 1 # unit: Seconds
DEFAULT_DISPLAY_OPTION = 0
LCD_BACKLIGHT_STATE = 0
TIME_BETWEEN_BEEPS = 1 # unit: Seconds

# These are for removing magic numbers. Really no reason to change them.
LCD_TOP_LINE = 1
LCD_BOTTOM_LINE = 2
LCD_LINE_LENGTH = 16 # unit: Characters
MIDNIGHT = 0
NOON = 12
SIX_PM = 18
EST = -5 # hours from UTC; eventually, make timezone calculation part of geo.py
