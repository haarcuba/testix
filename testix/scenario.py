from testix import testixexception
import pprint

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
			raise testixexception.ExpectationException( "unexpected call %s. Expected nothing" % self._formatActualCall( fakeObjectPath, args, kwargs ) )
		expected = self._expected.pop( 0 )
		if not expected.fits( fakeObjectPath, args, kwargs ):
			raise testixexception.ExpectationException( "unexpected call %s. Expected %s" % ( self._formatActualCall( fakeObjectPath, args, kwargs ), expected ) )
		return expected.result()

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
