import unittest
from testix.frequentlyused import *

import datetime
fakeModule( 'datetime' )

from examples import daylight
class FakeDay( object ):
	def __add__( self, other ):
		return other

class Test_Daylight( unittest.TestCase ):
	def test_Main( self ):
		scenario = Scenario()
		fakeDay = FakeDay()
		fakeDay.hour = 12
		scenario << \
			Call( 'datetime.date.today' ).returns( fakeDay ) << \
			Call( 'datetime.datetime.today' ).returns( fakeDay ) << \
			Call( 'datetime.timedelta', IgnoreArgument() ).returns( FakeDay() )
		nextDay = daylight.nextDaylightDate()
		self.assertTrue( nextDay is not fakeDay )
		scenario.end()

	def test_EarlyInTheMorningUsesSameDate( self ):
		scenario = Scenario()
		fakeDay = FakeDay()
		fakeDay.hour = 2
		scenario << \
			Call( 'datetime.date.today' ).returns( fakeDay ) << \
			Call( 'datetime.datetime.today' ).returns( fakeDay )
		nextDay = daylight.nextDaylightDate()
		self.assertTrue( nextDay is fakeDay )
		scenario.end()
