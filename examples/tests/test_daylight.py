from testix.frequentlyused import *

import datetime
fakeModule( 'datetime' )

from examples import daylight
class FakeDay( object ):
	def __add__( self, other ):
		return other

class Test_Daylight( testix.suite.Suite ):
	def test_Main( self ):
		scenario = Scenario()
		fakeDay = FakeDay()
		fakeDay.hour = 12
		scenario << \
			Call( 'datetime.date.today', [], fakeDay ) << \
			Call( 'datetime.datetime.today', [], fakeDay ) << \
			Call( 'datetime.timedelta', [ IgnoreArgument() ], FakeDay() )
		nextDay = daylight.nextDaylightDate()
		TS_ASSERT( nextDay is not fakeDay )
		scenario.end()

	def test_EarlyInTheMorningUsesSameDate( self ):
		scenario = Scenario()
		fakeDay = FakeDay()
		fakeDay.hour = 2
		scenario << \
			Call( 'datetime.date.today', [], fakeDay ) << \
			Call( 'datetime.datetime.today', [], fakeDay )
		nextDay = daylight.nextDaylightDate()
		TS_ASSERT( nextDay is fakeDay )
		scenario.end()
