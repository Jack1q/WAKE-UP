"""
wake-me-up
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import button_actions
import config
import constants
import logging
import processes
import threads

if __name__ == '__main__':

    if constants.DEBUG:
        config.begin_log()
        logging.info("Beginning clock")

    process_manager = processes.ProcessManager()
    process_manager.start_processes()
    threads.ThreadManager().start_threads()

    while True:
        c = input()
        if constants.VIRTUAL_HARDWARE and c == 'c':
            print('Virtual cycle button press.')
            print(f"Old display option: {config.get_settings_dictionary()['DISPLAY_OPTION']}")
            button_actions.cycle()
            print(f"New display option: {config.get_settings_dictionary()['DISPLAY_OPTION']}")

        else:
            if constants.DEBUG:
                logging.info("received keypress to shut off clock")
            process_manager.terminate_processes()
            break
