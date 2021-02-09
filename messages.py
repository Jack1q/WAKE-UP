""" Formatting for data collectors """
import time
from data_collection.weather import Weather
from data_collection.stocks import Stock
from data_collection.mail import Mail

def get_current_date():
    try:
        return time.strftime('%a %b %d, 20%y')
    except:
        return "Error"

def get_forecast():
    try:
        return Weather.get_latest_forecast()
    except:
        return "Error"

def get_stock(ticker):
    try:
        return Stock(ticker).get_stock_data()[:16]
    except:
        return "Error"

def get_unread(address, password):
    try:
        return Mail(address, password).get_unread_mail_count()
    except:
        return "Error"
