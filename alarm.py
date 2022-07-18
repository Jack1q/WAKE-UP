"""
wake-me-up
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import constants
import config
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
        if input():
            if constants.DEBUG:
                logging.info("received keypress to shut off clock")
            process_manager.terminate_processes()
            break
