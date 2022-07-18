""" Module for creating and managing button action functions """

import config
import constants
import logging
import messages


def cycle_bottom_lcd(settings_lock):
    """ Button function for cycling through bottom LCD display options """

    with settings_lock:
        if constants.DEBUG:
            logging.info("Cycle button pressed.")
        settings = config.get_settings_dictionary()
        settings['DISPLAY_OPTION'] = \
        (settings['DISPLAY_OPTION'] + 1) % len(messages.get_display_options())
        config.update_settings_file(settings)
