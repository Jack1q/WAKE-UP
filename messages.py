""" Formatting for data collectors """
import time
import data_collection.weather as weather
from data_collection.stocks import Stock
import data_collection.mail as mail
import data_collection.instagram as instagram
from data_collection.countdown import Countdown
from config import get_settings_dictionary

settings = get_settings_dictionary()

def get_current_time():
    try:
        return time.strftime('%I:%M %p %m/%d')
    except:
        return "Time Error"

def get_current_date():
    try:
        return time.strftime('%a %b %d, 20%y')
    except:
        return "Date Error"
    
def get_forecast():
    try:
        return weather.get_latest_forecast()[:16]
    except:
        return "Weather Error"
    
def get_stock():
    try:
        return Stock(settings['STOCK_TICKER']).get_stock_data()[:16]
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

def get_custom_message():
    return settings["CUSTOM_MESSAGE"][:16]

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
        get_custom_message,
        get_countdown
    ]