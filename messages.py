""" Formatting for data collectors """
import time
from data_collection.weather import Weather
from data_collection.stocks import Stock
from data_collection.mail import Mail
from data_collection.instagram import Instagram
from data_collection.countdown import Countdown
from config import Settings

class Messages:
    @staticmethod
    def get_current_time():
        try:
            return time.strftime('%I:%M %p %m/%d')
        except:
            return "Error"
    @staticmethod
    def get_current_date():
        try:
            return time.strftime('%a %b %d, 20%y')
        except:
            return "Error"
    @staticmethod
    def get_forecast():
        try:
            return Weather.get_latest_forecast()
        except:
            return "Error"
    @staticmethod
    def get_stock():
        try:
            return Stock(Settings.STOCK_TICKER).get_stock_data()[:16]
        except:
            return "Error"
    @staticmethod
    def get_unread():
        try:
            return Mail(Settings.EMAIL_ADDRESS, Settings.EMAIL_PASSWORD).get_unread_mail_count()
        except:
            return "Error"
    @staticmethod
    def get_instagram_followers():
        try:
            return Instagram(Settings.INSTAGRAM_USERNAME).get_follower_count()
        except:
            return "Error"
    @staticmethod
    def get_custom_message():
        return Settings.CUSTOM_MESSAGE[:16]
    @staticmethod
    def get_countdown():
        return Countdown(Settings.COUNTDOWN_DATETIME).get_formatted_countdown_message()