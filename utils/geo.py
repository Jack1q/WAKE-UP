""" module for geographical functions """

import requests
import logging

def get_client_ip_address():
    """ Retrieve's client's public IP address """
    # logging.info("getting client ip address")
    return requests.get('https://api64.ipify.org/').text

def get_latlong_from_ip_address(ip_address):
    """ Gets latitude and longitude from IP address """

    location_data = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    if 'error' in location_data and location_data['error']:
        logging.info("IP address location API error - %s", location_data['reason'])
        return None
    # logging.info("location data %s", location_data)
    return location_data['latitude'], location_data['longitude']
