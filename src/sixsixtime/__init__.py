import ephem
import datetime
from datetime import timedelta

def get_multiplier(total_seconds):
    return 43200/total_seconds

def get_time(in_time, lat, long):
    sun = ephem.Sun()
    somewhere = ephem.Observer()
    somewhere.date = in_time
    somewhere.lat = lat
    somewhere.lon = long
    if somewhere.previous_rising(sun) > somewhere.previous_setting(sun):
        multiplier = get_multiplier((somewhere.next_setting(sun).datetime()
                                    - somewhere.previous_rising(sun).datetime()
                                    ).total_seconds())
        seconds = ((in_time - somewhere.previous_rising(sun).datetime()).total_seconds()) * multiplier
        hours = (int((seconds / 60) / 60))
        seconds -= int((seconds / 60) / 60) * 60 * 60
        minutes = (int(seconds / 60))
        seconds -= int(seconds / 60) * 60
        in_time = in_time.replace(hour=(hours + 6), minute=minutes, second=int(seconds))
        return in_time
    else:
        multiplier = get_multiplier((somewhere.next_rising(sun).datetime()
                                    - somewhere.previous_setting(sun).datetime()
                                    ).total_seconds())
        seconds = ((in_time - somewhere.previous_setting(sun).datetime()).total_seconds()) * multiplier
        hours = (int((seconds / 60) / 60))
        seconds -= int((seconds / 60) / 60) * 60 * 60
        minutes = (int(seconds / 60))
        seconds -= int(seconds / 60) * 60
        if hours - 6 < 0:
            in_time -= datetime.timedelta(days=1)
            return in_time.replace(hour=(hours + 18), minute=minutes, second=int(seconds))
        return in_time.replace(hour=(hours - 6), minute=minutes, second=int(seconds))
