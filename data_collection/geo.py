""" module for geographical functions """

import requests

def get_client_ip_address():
    """ Retrieve's client's public IP address """

    return requests.get('https://api64.ipify.org/').text

def get_latlong_from_ip_address(ip_address):
    """ Gets latitude and longitude from IP address """

    location_data = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return location_data['latitude'], location_data['longitude']

