import datetime
import time
import sys
import re
import os

import dryscrape


class Prayer(object):
    def __init__(self, name):
        self.name = name

    def set_time(self, time):
        # time ==> hh:mm
        if not time or len(time) != 5 or time[2] != ':':
            self.hour = self.minute = None
            # log error

        self.time = time
        self.hour, self.minute = map(int, time.split(":"))

    def __repr__(self):
        return "Prayer({0}) - {1}".format(self.name, self.time)

    def __str__(self):
        return self.__repr__()


def get_dynamic_website(url):
    try:
        session = dryscrape.Session()
        session.visit(url)
        return session.body()

    # Excepting all Exception is bad. It is also bad to silently ignore/pass the exception.
    # so you should modify this. This is only a placeholder.
    except Exception as e:
        # log error
        pass


class Prayers(object):
    def __init__(self):
        self.is_updated_today = False
        names_of_prayers = ["fajr", "shurooq", "dhuhr", "asr", "maghrib", "isha"]
        self.data = [Prayer(name) for name in names_of_prayers]
        self.update_schedule()

    def _load_icci_schedule(self):
        html_prayers_schedule = get_dynamic_website("http://islamireland.ie/timetable/")
        for prayer in self.data:
            regex = re.compile('<span id="' + prayer.name + '-time" class="prayer-time">(.+?)</span>')
            prayer_time_result = re.findall(regex, html_prayers_schedule)
            prayer_time = prayer_time_result[0] if prayer_time_result else None
            prayer.set_time(prayer_time)

        print "prayers schedule was updated: {}".format(get_and_format_time_now())
        self.is_updated_today = True

    def update_schedule(self):
        self._load_icci_schedule()

    def play_adhan(self):
      operating_system = sys.platform
      if operating_system.startswith('linux'):
          os.system("mplayer adhan")
      else:
          print "Add code to play the Azhan. Currently this is an unsupport Operating System!"

    def is_prayer_time(self, now):
        for prayer in self.data:
            if prayer.hour == now.hour and prayer.minute == now.minute:
                return True

        return False

    def __repr__(self):
        return '\n'.join([str(prayer) for prayer in self.data])

    def __str__(self):
        return self.__repr__()


def get_and_format_time_now(custom_format="%d-%b-%Y %H:%M:%S"):
    return datetime.datetime.now().strftime(custom_format)


def continuously_check_prayer_time(prayers):
    print "Starting the main loop: {}".format(get_and_format_time_now())

    while 1:
        now = datetime.datetime.now()

        if not prayers.is_updated_today:
            prayers.update_schedule()

        elif now.hour == 0 and now.minute == 0:
            prayers.is_updated_today = False

        if prayers.is_prayer_time(now):
            prayers.play_adhan()

        time.sleep(50)


def main():
    prayers = Prayers()
    try:
        continuously_check_prayer_time(prayers)
    except KeyboardInterrupt:
        print "User interruption. Goodbye!"


if __name__ == '__main__':
    main()
