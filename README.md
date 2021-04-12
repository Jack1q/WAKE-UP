# MyPiClock v0.4
This repository contains the code for operating my Raspberry Pi alarm clock.

Feel free to clone this code for your own use, or fork this repository and make a pull request if there's anything you'd like to see added.

### Right now, this clock can:
- Tell the time
- Beep at a scheduled time on selected days of the week
- Display live stock prices from Yahoo Finance
- Display the local temperature and weather forecast 
- Tell you how many unread emails you have in your Gmail inbox
- Tell you your live Instagram follower count
- Display a custom message.
- Count down until a certain day / time.

### What I'm planning to add
- Displaying start/end times for online classes as they happen
- Showing pre-programmed holiday messages
- Multiple beep times within one day
- Beeping on specific calendar dates


### Bugs to fix / To-do list
- Parsing one-word forecast from National Weather API's shortForecast description
  - Right now, it just displays he shortForecast. Instead of 'Mostly Clear then Light Clouds' it should be 'Clear' because the LCD can only fit 16 chars on a line

### Contributing
Want to add a feature? Create a pull request!
