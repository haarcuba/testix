from testix import fakeobject
from testix import testixexception
from testix.startertests import startertestcollection
from testix.startertests.asserts import *

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
		
StarterTestFakeObject()
