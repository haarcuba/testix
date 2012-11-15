from testix import testixexception
import pprint

class Scenario( object ):
	_current = None

	def __init__( self ):
		if Scenario._current is not None:
			raise testixexception.TestixException( "New scenario started before previous one ended" )
		self._expected = []
		self._unorderedExpectations = set()
		Scenario._current = self

	def addCall( self, call ):
		if call.unordered():
			self._unorderedExpectations.add( call )
		else:
			self._expected.append( call )

	def resultFor( self, fakeObjectPath, * args, ** kwargs ):
		unorderedCall = self._findUnorderedCall( fakeObjectPath, args, kwargs )
		if unorderedCall is not None:
			return unorderedCall.result()

		return self._resultForOrderedCall( fakeObjectPath, args, kwargs )

	def _resultForOrderedCall( self, fakeObjectPath, args, kwargs ):
		if len( self._expected ) == 0:
			raise testixexception.ExpectationException( "unexpected call %s. Expected nothing" % self._formatActualCall( fakeObjectPath, args, kwargs ) )
		expected = self._expected.pop( 0 )
		self._verifyCallExpected( expected, fakeObjectPath, args, kwargs )
		return expected.result()

	def _findUnorderedCall( self, fakeObjectPath, args, kwargs ):
		for call in self._unorderedExpectations:
			if call.fits( fakeObjectPath, args, kwargs ):
				if not call.everlasting():
					self._unorderedExpectations.remove( call )
				return call
		return None

	def _verifyCallExpected( self, expected, fakeObjectPath, args, kwargs ):
		if not expected.fits( fakeObjectPath, args, kwargs ):
			raise testixexception.ExpectationException( "unexpected call %s. Expected %s" % ( self._formatActualCall( fakeObjectPath, args, kwargs ), expected ) )

	def _formatActualCall( self, fakeObjectPath, args, kwargs ):
		argsString = ', '.join( [ pprint.pformat( arg ) for arg in args ] )
		if len( kwargs ) > 0:
			kwargsString = ', '.join( '%s = %s' % ( key, pprint.pformat( val ) ) for (key, val) in kwargs.iteritems() )
			return '%s( %s, %s )' % ( fakeObjectPath, argsString, kwargsString )
		else:
			return '%s( %s )' % ( fakeObjectPath, argsString )
		
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
