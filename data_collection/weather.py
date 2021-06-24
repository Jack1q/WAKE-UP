""" Accesses local weather data for the clock to occasionally scroll through """
import requests
from data_collection.database import Database, Column
from datetime import datetime

def get_client_ip_address():
    """ Retrieve's client's public IP address """
    return requests.get('https://api64.ipify.org/').text

def get_latlong_from_ip_address(ip_address):
    """ Gets latitude and longitude from IP address """
    location_data = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return f"{location_data['latitude']},{location_data['longitude']}"

def get_weather_data_from_latlong(latlong):
    """ Accesses local weather data from the National Weather Service's API """
    # weather_data = requests.get('https://www.metaweather.com/api/location/search/?lattlong={}')
    grid_endpoint = requests.get(f'https://api.weather.gov/points/{latlong}').json()
    forecast_endpoint = requests.get(grid_endpoint['properties']['forecast']).json() 
    
    next_forecast = forecast_endpoint['properties']['periods']
    temperature = str(next_forecast[0]['temperature']) + 'F'
    forecast_description = next_forecast[0]['shortForecast']

    return temperature + ' ' + forecast_description

def create_weather_db():
    """ Creates new Database for storing Forecast data """
    db = Database()
    db.create_new_table(table_name = 'Forecasts',
        columns = [
            Column('Description','TEXT')
        ])

def get_db_forecast_value():
    """ 
    Retrieves most recently stored forecast value.
    With how data is stored into the Forecasts table in store_forecast_in_db()
    func (adds new row if none exists, otherwise updates row), there should only 
    ever really be one row and thus one value.
    """
    db = Database()
    return db.get_value_from_table('Forecasts', 'Description')[-1][0]

def store_forecast_in_db(new_forecast, is_first_value):
    """ 
    Stores forecast data into database. Adds a new row if none exists, otherwise update
    the single row for holding forecast Description data. 
    """
    db = Database()
    if is_first_value:
        db.add_to_table('Forecasts', [Column('Description','TEXT',new_forecast)])
    else:
        db.update_value('Forecasts', Column('Description','TEXT',get_db_forecast_value()), new_forecast)

def get_latest_forecast():
    """ Accesses latest local forecast data. Updates forecast every 10 minutes."""
    create_weather_db()
    database_is_empty = bool(Database().get_table_size('Forecasts') == 0)
    if (datetime.now().minute % 10 == 0 and datetime.now().second < 5) or database_is_empty: # updates every 10 minutes
        print('Getting new forecast...')
        ip = get_client_ip_address()
        latlong = get_latlong_from_ip_address(ip)
        weather_data = get_weather_data_from_latlong(latlong)
        store_forecast_in_db(weather_data, database_is_empty)
        return weather_data
    else:
        return get_db_forecast_value()
