""" Module for fetching your Instagram data """
import requests

def get_instagram_userdata(username):
    """ Fetches publicly available IG user data """
    return requests.get(f'https://www.instagram.com/{username}/?__a=1').json()

def get_follower_count(username):
    """ Returns follower count for given username """
    user_data = get_instagram_userdata(username)
    return "Insta: " + str(user_data['graphql']['user']['edge_followed_by']['count'])
