from testix import testixexception

class Scenario( object ):
	_current = None

	def __init__( self ):
		if Scenario._current is not None:
			raise testixexception.TestixException( "New scenario started before previous one ended" )
		self._expected = []
		Scenario._current = self

	def addCall( self, call ):
		self._expected.append( call )

	def resultFor( self, fakeObjectPath, * args, ** kwargs ):
		if len( self._expected ) == 0:
			raise testixexception.ExpectationException( "unexpected call '%s'( %s ). Expected nothing" % ( fakeObjectPath, args ) )
		expected = self._expected.pop( 0 )
		if not expected.fits( fakeObjectPath, args, kwargs ):
			raise testixexception.ExpectationException( "unexpected call '%s'( %s, kwargs = %s ). Expected %s" % ( fakeObjectPath, args, kwargs, expected ) )
		return expected.result()
		
	@staticmethod
	def current():
		return Scenario._current

	def end( self ):
		if len( self._expected ) > 0:
			raise testixexception.ExpectationException( "Scenario ended, but not all expectations were met. Pending expectations: %s" % self._expected )
		Scenario._current = None

	def __lshift__( self, expectation ):
		self.addCall( expectation )
		return self

def clearAllScenarios():
	Scenario._current = None

def current():
	return Scenario.current()
