""" Module for creating and managing button action functions """

import config
import messages


def cycle_bottom_lcd():
    """ Button function for cycling through bottom LCD display options """

    try:
        settings = config.get_settings_dictionary()
        settings['DISPLAY_OPTION'] = (settings['DISPLAY_OPTION'] + 1) % len(messages.get_display_options())
        config.update_settings_file(settings)
    except ValueError:
        pass
