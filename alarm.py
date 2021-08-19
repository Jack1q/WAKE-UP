""" 
wake-me-up
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import processes

def start_processes(process_list):
    for process in process_list:
        process.start()

def terminate_processes(process_list):
    for process in process_list:
        process.terminate()

if __name__ == '__main__':
    process_list = [
        processes.LCDProcess(),
        processes.BuzzerProcess(),
        processes.ButtonProcess(processes.ButtonActions.cycle_bottom_lcd, 10)    
        ]
    start_processes(process_list)
    while True:
        if input():
            termiante_processes(process_list)
            break