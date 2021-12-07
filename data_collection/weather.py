""" Module for fetching and storing local weather data based on IP address """

import datetime

import requests

from .database import Database, Column
from .geo import get_client_ip_address, get_latlong_from_ip_address


def get_weather_data_from_latlong(latitude, longitude):
    """ Accesses local weather data from the National Weather Service's API """
    # weather_data = requests.get('https://www.metaweather.com/api/location/search/?lattlong={}')
    grid_endpoint = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}').json()
    forecast_endpoint = requests.get(grid_endpoint['properties']['forecast']).json()

    next_forecast = forecast_endpoint['properties']['periods']
    temperature = str(next_forecast[0]['temperature']) + 'F'
    forecast_description = next_forecast[0]['shortForecast']

    return temperature + ' ' + forecast_description

def create_weather_db():
    """ Creates new Database for storing Forecast data """
    database = Database()
    database.create_new_table(table_name='Forecasts', columns=[Column('Description', 'TEXT')])

def get_db_forecast_value():
    """
    Retrieves most recently stored forecast value.
    With how data is stored into the Forecasts table in store_forecast_in_db()
    func (adds new row if none exists, otherwise updates row), there should only
    ever really be one row and thus one value.
    """
    database = Database()
    return database.get_value_from_table('Forecasts', 'Description')[-1][0]

def store_forecast_in_db(new_forecast, is_first_value):
    """
    Stores forecast data into database. Adds a new row if none exists, otherwise update
    the single row for holding forecast Description data.
    """
    database = Database()
    if is_first_value:
        database.add_to_table('Forecasts', [Column('Description', 'TEXT', new_forecast)])
    else:
        database.update_value('Forecasts', Column('Description', 'TEXT', get_db_forecast_value()),
                              new_forecast)

def get_latest_forecast():
    """ Accesses latest local forecast data. Updates forecast every 5 minutes. """

    create_weather_db()
    database_is_empty = bool(Database().get_table_size('Forecasts') == 0)
    current_time = datetime.datetime.now()
    minute, second = current_time.minute, current_time.second
    if (minute % 5 == 0 and second < 5) or database_is_empty:
        print('Getting new forecast...')
        ip_address = get_client_ip_address()
        latitude, longitude = get_latlong_from_ip_address(ip_address)
        weather_data = get_weather_data_from_latlong(latitude, longitude)
        store_forecast_in_db(weather_data, database_is_empty)
        return weather_data
    return get_db_forecast_value()

