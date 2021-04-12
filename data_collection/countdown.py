from datetime import datetime
class Countdown:
    """ Calculates time until a set time. """
    """ (also need to make alarm beep when countdown is finished) """

    def __init__(self, time_dictionary):
        """ 
        Parses COUNTDOWN_DATETIME dictionary into datetime object.
        dict should be formatted as:
            dict = {
                "year"  : 2000,
                "month" : 1,
                "day"   : 1,
                "hour"  : 0,
                "minute": 0
            }
        to match datetime() constructor args.
        """
        self.countdown_time = datetime(*time_dictionary.values())

    def get_time_delta(self):
        """ Calculates time from now until set countdown time """
        return self.countdown_time - datetime.now()
    
    def get_formatted_countdown_message(self):
        delta = self.get_time_delta()
        if delta.total_seconds() < 0:
            return "Countdown over."
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        if minutes < 10:
            minutes = "0" + str(minutes)
        seconds = (delta.seconds % 3600) % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        return f"{delta.days}d {hours}:{minutes}:{seconds}"
