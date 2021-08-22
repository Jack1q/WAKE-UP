""" Module for creating and managing button action functions """

import config
import messages


def cycle_bottom_lcd():
    """ Button function for cycling through bottom LCD display options """

    settings = config.get_settings_dictionary()
    option = settings['DISPLAY_OPTION']
    if option >= len(messages.get_display_options()) - 1:
        option = 0
    else:
        option += 1
    settings['DISPLAY_OPTION'] = option
    config.update_settings_file(settings)
