""" Formatting for data collectors """
import time
import datetime

import data_collection.weather as weather
from data_collection.stocks import Stock
import data_collection.mail as mail
import data_collection.instagram as instagram
from data_collection.countdown import Countdown
import config
import constants

settings = config.get_settings_dictionary()

def formatter(msg):
    if len(msg) < constants.LCD_LINE_LENGTH:
        return msg + (" " * (constants.LCD_LINE_LENGTH - len(msg)))
    if len(msg) > constants.LCD_LINE_LENGTH:
        return msg[:constants.LCD_LINE_LENGTH]
    return msg

def get_current_time():
    """ 
    Returns current time in format:
    'Hour:Minute AM|PM Month/Day'
    Example: '04:27 PM 02/09'
    """

    return time.strftime('%I:%M %p %m/%d')

def get_current_date():
    """ 
    Returns current date in format: 
    '{Weekday abbreviation} {Month abbreviation} {day}, {year} ' 
    Example: 'Fri Sep 3, 2021'
    """

    return time.strftime('%a %b %d, 20%y')
    
def get_forecast():
    try:
        return weather.get_latest_forecast()
    except:
        return "Weather Error"
    
def get_stock():
    try:
        return Stock(settings['STOCK_TICKER']).get_stock_data()
    except:
        return "Stock Error"

def get_unread():
    try:
        return mail.get_unread_mail_count(settings["EMAIL_ADDRESS"], settings["EMAIL_PASSWORD"])
    except:
        return "Email Error"

def get_instagram_followers():
    try:
        return instagram.get_follower_count(settings["INSTAGRAM_USERNAME"])
    except:
        return "IG Error"

def get_daily_message():
    today = time.strftime('%m-%d')
    daily_messages = settings['DAILY_MESSAGES']
    if today in daily_messages:
        return daily_messages[today]
    hour = datetime.datetime.now().hour
    if constants.MIDNIGHT <= hour < constants.NOON:
        return "Good Morning"
    elif constants.NOON <= hour < constants.SIX_PM:
        return "Good Afternoon"
    return "Good Night"    

def get_custom_message():
    return settings["CUSTOM_MESSAGE"]

def get_countdown():
    return Countdown(settings["COUNTDOWN_DATETIME"]).get_formatted_countdown_message()

def get_display_options():
    """ Returns list of display options for BOTTOM ROW """

    return [
        get_current_date,
        get_forecast,
        get_stock,
        get_unread,
        get_instagram_followers,
        get_daily_message,
        get_custom_message,
        get_countdown
    ]
