"""
WARNING: CODE BELOW WAS RUSHED, AND IS THUS VERY MESSY. READ AT OWN DANGER
sunrise/sunset calculation module
code adapted from:
	https://en.wikipedia.org/wiki/Sunrise_equation#Generalized_equation
    and
    https://gml.noaa.gov/grad/solcalc/solareqns.PDF
"""

import datetime
from math import sin, cos, tan, acos, pi

from geo import get_client_ip_address, get_latlong_from_ip_address


def is_leap(year):
    """ returns whether year is a leap year """

    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

def get_fractional_year(timetuple=None):
    if timetuple is None:
        timetuple = datetime.datetime.now().timetuple()
    day_of_year = timetuple.tm_yday
    hour = timetuple.tm_hour
    days_in_year = 365 + (1 if is_leap(timetuple.tm_year) else 0)
    return 2 * pi / days_in_year * (day_of_year - 1 + (hour - 12) / 24)

def get_equation_of_time(gamma):
    """ estimates eq of time in minutes """

    return 229.18*(0.000075 + 0.001868 * cos(gamma) - 0.032077 * sin(gamma) - \
        0.014615 * cos(2 * gamma) - 0.040849 * sin(2 * gamma))

def get_solar_declination_angle(gamma):
    """ estimates solar declination angle in radians """

    return 0.006918 - 0.399912 * cos(gamma) + 0.070257 * sin(gamma) - \
        0.006758 * cos(2 * gamma) + 0.000907 * sin(2 * gamma) - \
        0.002697 * cos(3 * gamma) + 0.00148 * sin(3 * gamma)
    
def get_time_offset(eqtime, longitude, timezone):
    """
    estimate time offset, in min: 
    eqtime in minutes, long in degrees, timezone in hours from UTC
    """

    return eqtime + 4 * longitude - 60 * timezone

def get_true_solar_time(timetuple, time_offset):
    """ gets tst in minutes """

    if timetuple is None:
        timetuple = datetime.datetime.now().timetuple()
    return timetuple.tm_hour * 60 + timetuple.tm_min + timetuple.tm_sec / 60 + time_offset

def get_sunrise_hour_angle(latitude, decl):
    """ calculates hour angle at sunrise in radians """
    return acos((cos(90.833 * pi / 180) / (cos(latitude * pi / 180) * cos(decl))) - \
        tan(latitude * pi / 180) * tan(decl))

def get_sunrise(longitude, hour_angle, eqtime):
    """ gets time of sunrise in minutes """

    return 720 - 4 * (longitude + hour_angle * 180 / pi) - eqtime

def get_sunset(longitude, hour_angle, eqtime):
    return 720 - 4 * (longitude - hour_angle * 180 / pi) - eqtime

def formatted_local_sunsetrise(is_sunrise, utc):
    latitude, longitude, = get_latlong_from_ip_address(get_client_ip_address())
    gamma = get_fractional_year()
    decl = get_solar_declination_angle(gamma)
    eqtime = get_equation_of_time(gamma)
    hour_angle = get_sunrise_hour_angle(latitude, decl)
    if is_sunrise:
        mins = get_sunrise(longitude, hour_angle, eqtime)
    else:
        mins = get_sunset(longitude, hour_angle, eqtime)
    hour = mins / 60 + utc
    mins = int(60 * (hour - int(hour)))
    hour = int(hour)
    if mins < 10:
        mins = '0' + str(mins)
    return f'{hour}:{mins}'

if __name__ == '__main__':

    print(formatted_local_sunsetrise(False, -5))
