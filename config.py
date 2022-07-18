""" Module for managing configuration / settings """

import json
import logging

def get_json_dictionary(filename):
    """
    Retrieves dictionary from json file.
    """

    with open(filename, 'r') as file:
        return json.load(file)

def update_json_file(filename, updated_dictionary):
    """ Saves updated dict to json file """

    with open(filename, 'w') as file:
        file.write(json.dumps(updated_dictionary, indent=4))


def get_settings_dictionary():
    """
    Retrieves settings dictionary.
    Note: SLEEP_IN_DAYS day notation works as follows: Mon = 0, Tue = 1, ... , Sun = 6
    """

    return get_json_dictionary('settings.json')


def update_settings_file(updated_dictionary):
    """ Saves updated settings dict to settings.json """

    update_json_file('settings.json', updated_dictionary)


def get_data_dictionary():
    """ retrieves data json as dictionary """

    return get_json_dictionary('data.json')

def update_data_file(updated_dictionary):
    """ Saves updated data dict to data.json """

    update_json_file('data.json', updated_dictionary)

def begin_log():
    logging.basicConfig(filename="alarm.log", level=logging.INFO)

