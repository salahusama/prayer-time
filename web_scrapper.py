'''
	Salaheldin Akl
	
	Program to extract data from webpage
	Times of prayer extracted as a string
	Then converted to int
	Webpage source: http://islamireland.ie/timetable/
'''

import dryscrape
import datetime
import time
import re
import os

class Prayer:
	name = ''
	strTime = ''
	hour = 0
	minute = 0

	def __init__(self, name):
		self.name = name

def parse(p):
	# strTime = hh:mm
	strHour = p.strTime[0:2]
	strMin = p.strTime[3:6]
	p.hour = int(strHour)
	p.minute = int(strMin)

def update():
	# get website data
	session = dryscrape.Session()
	session.visit("http://islamireland.ie/timetable/")
	response = session.body()

	# add time info to prayer objects
	for p in pList:
		regex = '<span id="' + p.name + '-time" class="prayer-time">(.+?)</span>'
		find = re.compile(regex)
		p.strTime = re.findall(find, response)[0]
		# turn time from string to int
		parse(p);

# create prayer objects in a list
prayer = ["fajr","shurooq","dhuhr","asr","maghrib","isha"]
pList = []

# time not updated at start of program
updated_today = False

for i in range(6):
	pList.append( Prayer(prayer[i]) )

# continuously running program
while(1):
	# get current time
	now = datetime.datetime.now()

	# update time once a day
	if not updated_today:
		update()
		updated_today = True
		print str(now)[:19], "updated..."
	
	elif now.hour == 0 and now.minute == 0:
		# new day, so time not updated
		updated_today = False

	print str(now)[:19], "running..."

	# check if time for any prayer
	for p in pList:
		if p.hour == now.hour and p.minute == now.minute:
			print str(now)[:19], "adhan..."
			os.system("mplayer adhan")
	# execute every minute
	time.sleep(50)
