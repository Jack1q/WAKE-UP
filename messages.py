""" Formatting for data collectors """
import time
import data_collection.weather as weather
from data_collection.stocks import Stock
import data_collection.mail as mail
import data_collection.instagram as instagram
from data_collection.countdown import Countdown
from config import Settings

def get_current_time():
    try:
        return time.strftime('%I:%M %p %m/%d')
    except:
        return "Error"

def get_current_date():
    try:
        return time.strftime('%a %b %d, 20%y')
    except:
        return "Error"
    
def get_forecast():
    try:
        return weather.get_latest_forecast()[:16]
    except:
        return "Error"
    
def get_stock():
    try:
        return Stock(Settings.STOCK_TICKER).get_stock_data()[:16]
    except:
        return "Error"

def get_unread():
    try:
        return mail.get_unread_mail_count(Settings.EMAIL_ADDRESS, Settings.EMAIL_PASSWORD)
    except:
        return "Error"

def get_instagram_followers():
    try:
        return instagram.get_follower_count(Settings.INSTAGRAM_USERNAME)
    except:
        return "Error"

def get_custom_message():
    return Settings.CUSTOM_MESSAGE[:16]

def get_countdown():
    return Countdown(Settings.COUNTDOWN_DATETIME).get_formatted_countdown_message()
    