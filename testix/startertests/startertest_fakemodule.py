from testix import scenario
from testix import expectations
from testix.startertests.asserts import *
from testix import fakemodule
from testix import fakeobject
from testix.startertests import startertestcollection

fakemodule.fakeModule( 'socket' )
import fakemoduleimporter

class StarterTestFakeModule( startertestcollection.StarterTestCollection ):
	def starter_test_FakeSocketCreated( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'socket.socket', [], 'fake_value' )
		fakeModuleUser = fakemoduleimporter.FakeModuleUser()
		fakeModuleUser.createSocket()
		STS_ASSERT_EQUALS( fakeModuleUser.socket(), 'fake_value' )
		aScenario.end()

	def starter_test_FakeObjectVerification( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'socket.socket', [], fakeobject.FakeObject( 'fake socket' ) )
		fakeModuleUser = fakemoduleimporter.FakeModuleUser()
		fakeModuleUser.createSocket()
		STS_ASSERT_IS_FAKE_OBJECT( fakeModuleUser.socket(), 'fake socket' )
		aScenario.end()

	def starter_test_Bugfix_FakeOnlyOneSubmodule( self ):
		import fathermodule
		fakemodule.fakeModule( 'fathermodule.firstsubmodule' )
		from fathermodule import firstsubmodule
		from fathermodule import secondsubmodule
		STS_ASSERT( firstsubmodule is fakeobject.FakeObject( 'fathermodule.firstsubmodule' ) )
		STS_ASSERT( not isinstance( secondsubmodule, fakeobject.FakeObject ) )
		
StarterTestFakeModule()
