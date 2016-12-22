'''
   Salaheldin Akl

   Program to extract data from webpage
   Times of prayer extracted as a string
   Then converted to int
   Webpage source: http://islamireland.ie/timetable/
'''

'''
According to PEP8 http://pymbook.readthedocs.io/en/latest/pep8.html:

Imports should be grouped in the following order:

standard library imports
related third party imports
local application/library specific imports
You should put a blank line between each group of imports.
'''
import datetime
import time
import re
import os

#import dryscrape


'''
According to https://wiki.python.org/moin/NewClassVsClassicClass:

The new-style (e.g. Python > 2.1) for defining a class is: class Prayer(object).
It is the preferred way, you can read more by searching for (New VS Old style classes in Python).
'''
class Prayer:
    name = ''
    # 1) PEP8: Variable names should be lowercase with words separated by underscores as necessary to improve readability
    # 2) It's generally an anti-pattern in Python to include type notation (e.g. str) in the variable name.
    #    Python is "a duck-typed language", you shouldn't assume the type of the variable based on its name.
    # 3) Are you using the class only to store time/name information with no public/private methods? Do you want to
    #    use namedtuple instead? Or maybe add some methods to the class like (parse_time(..), & is_prayer_time(..))
    strTime = ''
    hour = 0
    minute = 0

    def __init__(self, name):
        self.name = name


# I would suggest choosing a better name for the function (usually a camelCase verb/noun pair.
# e.g. parsePrayer(prayer) or parsePrayerTime(prayer) etc.
def parse(p):
    # strTime = hh:mm
    # Same comment about variable name & type notation anti-pattern.
    strHour = p.strTime[0:2]
    strMin = p.strTime[3:6]
    p.hour = int(strHour)
    p.minute = int(strMin)
    # You probably could rewrite the function as follows:
    #
    # def parse_and_store_prayer_time(prayer):
    #     prayer.hour, prayer.minute = map(int, prayer.time.split(":"))
    #
    # You could also include some checking like (if not prayer: return) and/or Exception handling and logging



def update():
    # I would suggest choosing a better name for the function. Is 'update()' descriptive enough?
    #  Don't be afraid to make a name long. A long descriptive name is better than a short enigmatic one.


    '''
    maybe something like:

     def get_dynamic_website(url="http://islamireland.ie/timetable/"):
        session = dryscrape.Session()
        session.visit(url)
        return session.body()

    '''
    # get website data

    # I will hardcode the below for now, so I can test quickly, as I failed to get dryscrape working on MacOS Sierra :(
    #session = dryscrape.Session()
    #session.visit("http://islamireland.ie/timetable/")
    #response = session.body()
    #html = response.read()
    html = """
    '<span id="fajr-time" class="prayer-time">01:23</span>'
    '<span id="shurooq-time" class="prayer-time">02:34</span>'
    '<span id="dhuhr-time" class="prayer-time">07:40</span>'
    '<span id="asr-time" class="prayer-time">13:42</span>'
    '<span id="maghrib-time" class="prayer-time">18:32</span>'
    '<span id="isha-time" class="prayer-time">21:03</span>'
    """

    # add time info to prayer objects
    for p in pList:
        regex = '<span id="' + p.name + '-time" class="prayer-time">(.+?)</span>'
        find = re.compile(regex)
        # You need Exception handling. What if no match was found? accessing [0] would break your script.
        p.strTime = re.findall(find, html)[0]
        # turn time from string to int
        # Python does not require semi-colons to terminate statements.
        # Semi colons can be used to delimit statements if you wish to put multiple statements on the same line
        parse(p);


# list comprehension ? See below.
# create prayer objects in a list
prayer = ["fajr", "shurooq", "dhuhr", "asr", "maghrib", "isha"]
pList = []

# time not updated at start of program
updated_today = False


'''
You could use a list comprehension for simplicity:

names_of_prayers = ["fajr", "shurooq", "dhuhr", "asr", "maghrib", "isha"]
prayers = [Prayer(name) for name in names_of_prayers]

'''
for i in range(6):
    pList.append(Prayer(prayer[i]))

# continuously running program

# You don't need the parenthesis. While 1: should work.
while (1):

    '''
    You may want to consider a scheduler instead of checking every second if hour && minute match a prayer.
    Similar to what I have in my code. I think this is less CPU intensive
    '''

    # get current time
    now = datetime.datetime.now()

    # update time once a day
    if not updated_today:
        update()
        updated_today = True
        # I think it's better to use strftime() e.g. datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        print str(now)[:19], "updated..."

    elif now.hour == 0 and now.minute == 0:
        # new day, so time not updated
        updated_today = False

    # ditto. use strftime()
    print str(now)[:19], "running..."

    # check if time for any prayer
    for p in pList:
        if p.hour == now.hour and p.minute == now.minute:
            print str(now)[:19], "adhan..."
            # I would extract this to a separate function e.g. play_adhan(..) inside this function you can check the OS.
            # Based on the OS you can execute an appropriate command.
            # Something like:
            # def play_adhan():
            #   operating_system = os.platform
            #   if sys.platform.startswith('linux'):
            #       os.system("mplayer adhan")
            #   elif sys.platform.startswith('win')
            #       ...
            #   elif sys.platform.startswith('darwin')
            #       ...
            #   else:
            #       pass

            os.system("mplayer adhan")
    # execute every minute
    time.sleep(50)
