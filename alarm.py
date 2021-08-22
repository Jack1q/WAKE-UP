"""
wake-me-up
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import processes


if __name__ == '__main__':

    process_manager = processes.ProcessManager()
    process_manager.start_processes()

    while True:
        if input():
            process_manager.terminate_processes()
            break
