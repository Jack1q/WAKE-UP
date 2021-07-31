""" Module for managing configuration / settings """

import json


def get_settings_dictionary():
    """ 
    Retrieves settings dictionary. 
    Note: SLEEP_IN_DAYS day notation works as follows: Mon = 0, Tue = 1, ... , Sun = 6
    """

    with open('settings.json', 'r') as settings_file:
        return json.load(settings_file)


def update_settings_file(updated_dictionary):
    """ Saves updated settings dict to settings.json """

    with open('settings.json', 'w') as settings_file:
        settings_file.write(json.dumps(updated_dictionary, indent=4))
