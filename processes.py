""" Module for creating and managing Clock processes """


import config
import constants

import logging
import messages
import multiprocessing
import time

if not constants.VIRTUAL_HARDWARE:
    try:
        from display.lcd_display import LCD #, LCD_CLEARDISPLAY
    except ImportError as e:
        print("Could not import LCD module into processes", e)
        if constants.DEBUG:
            logging.info("error importing lcd module into processes: %s", e)



class LCDProcess(multiprocessing.Process):
    """ Process for manipulating and updating Clock screen with relevant data """

    if not constants.VIRTUAL_HARDWARE:
        lcd = LCD()
        lcd.backlight(constants.LCD_BACKLIGHT_STATE)

    def __init__(self):
        if constants.DEBUG:
            logging.info("starting LCD process")
        super().__init__(target=LCDProcess.update_lcd, args=(), daemon=True)

    @staticmethod
    def update_lcd():
        """ Constantly updates LCD screen with time and user's chosen data to track """
        config.begin_log()
        while True:
            # Top LCD Line:
            current_time = messages.get_current_time()
            if constants.VIRTUAL_HARDWARE:
                current_time +=  ' ' * (16 - len(current_time))
                print('VIRTUAL SCREEN:', '\n+' + '-' * 18 + '+\n|', current_time, '|')
            else:
                LCDProcess.lcd.lcd_display_string(current_time, constants.LCD_TOP_LINE)

            # Bottom LCD Line:
            display_options = messages.get_display_options()
            try:
                settings = config.get_settings_dictionary()
                selected_option = display_options[settings['DISPLAY_OPTION'] % len(display_options)]
            except ValueError:
                selected_option = display_options[constants.DEFAULT_DISPLAY_OPTION]
            message = messages.fix_length(selected_option())
            if constants.VIRTUAL_HARDWARE:
                # add extra spaces to message if needed so it fits virtual 'screen'
                message += ' ' * (16 - len(message))
                print('|', message, '|\n+' + '-' * 18 + '+')
            else:
                LCDProcess.lcd.lcd_display_string(message, constants.LCD_BOTTOM_LINE)
            if constants.VIRTUAL_HARDWARE:
                time.sleep(3)
    
    @staticmethod
    def clear_lcd():
        """ clears LCD screen """
        
        if not constants.VIRTUAL_HARDWARE:
            # LCDProcess.lcd.lcd_write(LCD_CLEARDISPLAY)
            blank_line = " " * 16
            LCDProcess.lcd.lcd_display_string(blank_line, constants.LCD_TOP_LINE)
            LCDProcess.lcd.lcd_display_string(blank_line, constants.LCD_BOTTOM_LINE)


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
        # Clear LCD
        if not constants.VIRTUAL_HARDWARE:
            LCDProcess.clear_lcd()
