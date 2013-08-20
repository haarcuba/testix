from testix.frequentlyused import *

fakeModule( 'common' )
fakeModule( 'common.waitforipcserver' )
fakeModule( 'connectionlogger' )
fakeModule( 'connectionlogger.ipc' )
from examples import bugfix

class Test_Calculator( testix.suite.Suite ):
	def construct( self ):
		scenario = Scenario() <<\
			Call( 'common.waitforipcserver.WaitForIPCServer', [ FakeObject( 'connectionlogger.ipc' ), FakeObject( 'connectionlogger.ipc.runnning_Remote' ) ], None, kwargExpectations = { 'remoteHost': '10.20.20.1' } )
		self.tested = bugfix.BugFix()
		scenario.end()

	def test_Go( self ):
		self.construct()
