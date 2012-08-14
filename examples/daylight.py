import datetime

def _beforeDawn( hour ):
	EARLY = 5
	return hour < EARLY

def nextDaylightDate():
	today = datetime.date.today()
	hour = datetime.datetime.today().hour
	if _beforeDawn( hour ):
		return today
	else:
		return today + datetime.timedelta( 1 )
