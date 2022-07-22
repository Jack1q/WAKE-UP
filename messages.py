"""
The purpose of this module is to prepare data received from data
collector modules to be properly displayed on the clock screen.
Each function returns display data, and prints any error messages
to terminal output.
"""

import time
import datetime
import logging

from utils.stocks import Stock
import utils.mail as mail
import utils.instagram as instagram
from utils.countdown import Countdown
import config
import constants

def get_settings():
    """ returns settings dict """

    return config.get_settings_dictionary()

def get_data():
    """ returns data dict """

    return config.get_data_dictionary()

def fix_length(message):
    """ Ensures message length equals LCD_LINE_LENGTH """

    if len(message) < constants.LCD_LINE_LENGTH:
        return message + (" " * (constants.LCD_LINE_LENGTH - len(message)))
    if len(message) > constants.LCD_LINE_LENGTH:
        return message[:constants.LCD_LINE_LENGTH]
    return message

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
    """ Returns weather forecast message """
    try:
        data = get_data()['forecast']
    except Exception as e:
        logging.info("error fetching weather data: %s", e)
        return "Weather Error"
    if data == None:
        return "Weather Error"
    return data

def get_sun():
    """ returns sunrise/sunset message """
    try:
        data = get_data()
        return "Sun: " + data['sunrise'] + "|" + data['sunset']
    except Exception as e:
        logging.info("error fetching sunset & sunrise data: %s", e)
        return "sunset error"

def get_stock():
    """ Returns stock data message"""

    try:
        settings = get_settings()
        data = Stock(settings['STOCK_TICKER']).get_stock_data()
    except Exception as e:
        return "Stock error"
    if data == None:
        return "Stock error"
    return data

def get_unread():
    """ Returns unread email count message """

    try:
        settings = get_settings()
        unread = mail.get_unread_mail_count(settings["EMAIL_ADDRESS"],
                                          settings["EMAIL_PASSWORD"])
    except Exception as e:
        return "Email Error"
    if unread == None:
        return "Email Error"
    return unread


def get_instagram_followers():
    """ Returns IG follow count message """

    try:
        count = instagram.get_follower_count(get_settings()["INSTAGRAM_USERNAME"])
    except Exception as e:
        return "IG Error"
    if count == None:
        return "IG Error"
    return count

def get_daily_message():
    """ Returns daily message if one exists, otherwise time-based greeting """

    today = time.strftime('%m-%d')
    daily_messages = get_settings()['DAILY_MESSAGES']
    if today in daily_messages:
        return daily_messages[today]
    hour = datetime.datetime.now().hour
    if constants.MIDNIGHT <= hour < constants.NOON:
        return "Good Morning"
    if constants.NOON <= hour < constants.SIX_PM:
        return "Good Afternoon"
    return "Good Night"

def get_custom_message():
    """ Returns custom message from settings """

    return get_settings()["CUSTOM_MESSAGE"]

def get_countdown():
    """ Returns countdown message """

    return Countdown(get_settings()["COUNTDOWN_DATETIME"]).get_pretty_countdown_message()

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
        get_countdown,
        get_sun
    ]
