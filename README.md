# MyPiClock v0.4
This repository contains the code for operating my Raspberry Pi alarm clock.

### Right now, this clock can:
- Tell the time
- Beep at a scheduled time on selected days of the week
- Display live stock prices from Yahoo Finance
- Display the local temperature and weather forecast 
- Tell you how many unread emails you have in your Gmail inbox

### What I'm planning to add
- Displaying start/end times for online classes as they happen
- Showing pre-programmed holiday messages
- Multiple beep times within one day
- Beeping on specific calendar dates


### Bugs to fix / other tasks
- Parsing one-word forecast from National Weather API's shortForecast description
  - Right now, it just displays he shortForecast. Instead of 'Mostly Clear then Light Clouds' it should be 'Clear' because the LCD can only fit 16 chars on a line
