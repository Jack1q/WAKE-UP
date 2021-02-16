import requests

class Instagram:
    """ Class for fetching your Instagram data """
    def __init__(self, username):
        self.username = username
    
    def get_instagram_userdata(self):
        """ Fetches publicly available IG user data """
        return requests.get(f'https://www.instagram.com/{self.username}/?__a=1').json()
    
    def get_follower_count(self):
        """ Returns follower count for given username """
        user_data = self.get_instagram_userdata()
        return "Insta: " + str(user_data['graphql']['user']['edge_followed_by']['count'])
