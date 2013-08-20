import types
from testix import fakeobject

class Suite( object ):
	def __init__( self ):
		self._totalRun = 0

	def run( self ):
		tests = self._findTests()
		for test in tests:
			self._totalRun += 1
			fakeobject.clearNonModuleFakeObjects()
			self.setup()
			test()
			self.teardown()

	def totalTestsRun( self ):
		return self._totalRun

	def _findTests( self ):
		tests = []
		for name in type( self ).__dict__:
			testCandidate = getattr( self, name )
			if type( testCandidate ) is types.MethodType:
				if name.startswith( 'test_' ):
					tests.append( testCandidate )
		return tests

	def setup( self ):
		pass

	def teardown( self ):
		pass
