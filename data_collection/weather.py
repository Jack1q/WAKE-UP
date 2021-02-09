import requests

class Weather:
    """ Accesses local weather data for the clock to occasionally scroll through """

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

    def get_latest_forecast():
        """ Accesses latest local forecast data. Database is used if data is still fresh """
        ip = Weather.get_client_ip_address()
        latlong = Weather.get_latlong_from_ip_address(ip)
        weather_data = Weather.get_weather_data_from_latlong(latlong)
        return weather_data # (Temporary)
        pass
        """ Must add method to shorten forecast + only refresh every 5 minutes"""
        # store forecast + time in sqlite.
        # if time > 3 hours ago, get new forecast and store it
        # else, get stored forecast.
