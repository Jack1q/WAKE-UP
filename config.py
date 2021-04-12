""" Configurable constants for easy access """

""" Don't change date constants """
class Day:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7) 

""" Change the default values below to whatever you want """
class Settings:
    SLEEP_IN_DAYS = [Day.SATURDAY, Day.SUNDAY]
    HOUR = 6
    MINUTES = 30
    EMAIL_ADDRESS = ""
    EMAIL_PASSWORD = ""
    STOCK_TICKER = "GME"
    CUSTOM_MESSAGE = "Hello world!"
    INSTAGRAM_USERNAME = "instagram"
    COUNTDOWN_DATETIME = {
        "year" : 2022,
        "month" : 1,
        "day" : 1,
        "hour" : 0,
        "minute" : 0
    }