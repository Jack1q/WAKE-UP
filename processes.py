""" Module for creating and managing Clock processes """

import multiprocessing

import config
import constants
from display.lcd_display import LCD
import logging
import messages




class LCDProcess(multiprocessing.Process):
    """ Process for manipulating and updating Clock screen with relevant data """

    lcd = LCD()
    lcd.backlight(constants.LCD_BACKLIGHT_STATE)

    def __init__(self):
        if constants.DEBUG:
            logging.info("starting LCD process")
        super().__init__(target=LCDProcess.update_lcd, args=(), daemon=True)

    @staticmethod
    def update_lcd():
        """ Constantly updates LCD screen with time and user's chosen data to track """

        while True:

            # Top LCD Line:
            LCDProcess.lcd.lcd_display_string(messages.get_current_time(), constants.LCD_TOP_LINE)

            # Bottom LCD Line:
            display_options = messages.get_display_options()
            try:
                settings = config.get_settings_dictionary()
                selected_option = display_options[settings['DISPLAY_OPTION'] % len(display_options)]
            except ValueError:
                selected_option = display_options[constants.DEFAULT_DISPLAY_OPTION]
            message = messages.fix_length(selected_option())
            LCDProcess.lcd.lcd_display_string(message, constants.LCD_BOTTOM_LINE)


class ProcessManager:
    """ Class for managing all Clock processes """

    def __init__(self):
        self.processes_in_use = [
            LCDProcess()
        ]

    def start_processes(self):
        """ Starts all processes in use """
        if constants.DEBUG:
            logging.info("starting processes")
        for process in self.processes_in_use:
            process.start()

    def terminate_processes(self):
        """ Terminates all processes in use """
        if constants.DEBUG:
            logging.info("terminating processes")
        for process in self.processes_in_use:
            process.terminate()
