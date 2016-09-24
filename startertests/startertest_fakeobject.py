from testix import fakeobject
from testix import testixexception
from startertests import startertestcollection
from startertests.asserts import *
from testix import scenario
from testix import expectations
from testix import fakemodule
import sys

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
		fakeobject.clearNonModuleFakeObjects()
		STS_ASSERT( fake1 is not fakeobject.FakeObject( "one" ) )
		STS_ASSERT( fake2 is not fakeobject.FakeObject( "two" ) )

	def starter_test_ClearOnlyNonModuleObjects( self ):
		fake1 = fakeobject.FakeObject( "one" )
		fakemodule.fakeModule( 'mymodule' )
		fakeModule = sys.modules[ 'mymodule' ]
		STS_ASSERT( fake1 is fakeobject.FakeObject( "one" ) )
		STS_ASSERT( fakeModule is fakeobject.FakeObject( "mymodule" ) )
		fakeobject.clearNonModuleFakeObjects()
		STS_ASSERT( fake1 is not fakeobject.FakeObject( "one" ) )
		STS_ASSERT( fakeModule is fakeobject.FakeObject( "mymodule" ) )

StarterTestFakeObject()
