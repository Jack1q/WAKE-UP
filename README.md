# alarmpi
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
- Show configurable messages on certain days, such as ```Happy Birthday``` or ```Happy Pi Day!```
- Count down until a certain date and/or time.
- Display the local sunset / sunrise times.

### Additional features
- Flask web dashboard to customize clock settings
- Play YouTube audio instead of buzzer for wakeup

## Setup

### Hardware
- Raspberry Pi 4 (Other versions should work, but I've yet to test it on anything else.)
- I2C 16x2 LCD Display Module
- 5V Piezoelectric Buzzer
- Mini Pushbutton Switches
- Jumper Wires (M-M, M-F)
- 10K Ohm Resistor

I will post a circuit diagram once I'm finished making it.

Also, GPIO pins can be configured in ```constants.py```. In case you're wondering,
I've placed settings that I plan on allowing users to change while the clock is operating via a web dashboard in ```settings.json``` and settings that should not be changed during operation in ```constants.py```, as I hope to use the web application to send the ```json``` data to the Pi (with proper security
precautions taken).

### Software
To install the required modules, run ```pip3 install -r requirements.txt```.

Then run

```sudo apt-get install python3-smbus``` and 
```sudo apt-get install rpi.gpio```

Configure as much as you'd like in ```settings.json```, then run ```python3 alarm.py```


### Contributing
Want to add a feature or fix a bug you've noticed? Create a pull request!!

![image](https://i.imgur.com/kwc1tPG.jpg)

Clock photo as of February, 2021



![image](https://i.imgur.com/DcT7nkX.png)


Dashboard photo 8/2022


