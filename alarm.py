""" 
wake-me-up
Smart LCD Alarm Clock with wake-up piezo buzzer.
Contributor List: Jack Donofrio
Last updated on April 11, 2021 at 2:52 PM.
"""

import processes

if __name__ == '__main__':
    lcd_process = processes.LCDProcess()
    beep_process = processes.BuzzerProcess()
    lcd_process.start()
    beep_process.start()
    while True:
        if input():
            lcd_process.terminate()
            beep_process.terminate()
            break