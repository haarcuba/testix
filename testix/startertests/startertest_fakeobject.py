from testix import fakeobject
from testix import testixexception
from testix.startertests import startertestcollection
from testix.startertests.asserts import *
from testix import scenario
from testix import expectations

class StarterTestFakeObject( startertestcollection.StarterTestCollection ):
	def starter_test_CallingFakeObject_WhileNoScenario_MustThrow( self ):
		fakeObject = fakeobject.FakeObject( 'hi there' )	
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.TestixException, fakeObject )

	def starter_test_FakeObjectImplicitCreation_OnlyOnce( self ):
		fakeObject = fakeobject.FakeObject( 'hi there' )	
		b1 = fakeObject.b
		b2 = fakeObject.b
		STS_ASSERT( b1 is b2 )

	def starter_test_FakeObjectCreation_OnlyOnce( self ):
		fakeObject1 = fakeobject.FakeObject( 'hi there' )
		fakeObject2 = fakeobject.FakeObject( 'hi there' )
		STS_ASSERT( fakeObject1 is fakeObject2 )

	def starter_test_FakeBuiltinObject( self ):
		fakeobject.fakeBuiltIn( 'open' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'open', [ 'some_file' ], 1234 )
		STS_ASSERT_EQUALS( open( 'some_file' ), 1234 )
		aScenario.end()

	def starter_test_ClearAllFakeObjects( self ):
		fake1 = fakeobject.FakeObject( "one" )
		fake2 = fakeobject.FakeObject( "two" )
		STS_ASSERT( fake1 is fakeobject.FakeObject( "one" ) )
		STS_ASSERT( fake2 is fakeobject.FakeObject( "two" ) )
		fakeobject.clearAll()
		STS_ASSERT( fake1 is not fakeobject.FakeObject( "one" ) )
		STS_ASSERT( fake2 is not fakeobject.FakeObject( "two" ) )

		
StarterTestFakeObject()
