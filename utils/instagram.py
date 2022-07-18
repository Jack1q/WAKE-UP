""" Module for fetching your Instagram data """
import requests
import logging

def get_instagram_userdata(username):
    """ Fetches publicly available IG user data """
    return requests.get(f'https://www.instagram.com/{username}/?__a=1')

def get_follower_count(username):
    """ Returns follower count for given username """
    try:
        user_data = get_instagram_userdata(username).json()
        return "Insta: " + str(user_data['graphql']['user']['edge_followed_by']['count'])
    except Exception as e:
        logging.error("could not fetch instagram followers from API: %s", e)
        return "IG Error"