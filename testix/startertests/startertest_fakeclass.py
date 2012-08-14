from testix.frequentlyused import *
from testix.startertests import startertestcollection

fakeModule( 'bogusmodule' )
fakeClass( module = 'bogusmodule', className = 'BogusClass' )

import fakeclassderiver

class StarterTestFakeClass( startertestcollection.StarterTestCollection ):
	def starter_test_FakeABaseClass( self ):
		scenario = Scenario() <<\
			Call( 'bogusmodule.BogusClass', [ 'one', 'two' ], None )
		derived = fakeclassderiver.Derived( 'one', 'two' )
		scenario.end()

StarterTestFakeClass()
