from testix import testixexception
from testix import hook
import pprint
import sys

class Scenario( object ):
    _current = None

    def __init__( self, verbose = False ):
        if Scenario._current is not None:
                raise testixexception.TestixException( "New scenario started before previous one ended" )
        self._verbose = verbose
        self._expected = []
        self._unorderedExpectations = set()
        self._endingVerifications = True
        Scenario._current = self

    def __enter__( self ):
        return self

    def __exit__( self, type, value, traceback ):
        if type is not None:
            self._endingVerifications = False
        self.end()

    def _debug( self, message ):
        if not self._verbose:
                return
        sys.stderr.write( '%s\n' % message )

    def addEvent( self, event ):
        if isinstance( event, hook.Hook ):
                self._expected.append( event )
                return
        call = event
        if call.unordered_():
                self._unorderedExpectations.add( call )
        else:
                self._expected.append( call )

    def resultFor( self, fakeObjectPath, * args, ** kwargs ):
        unorderedCall = self._findUnorderedCall( fakeObjectPath, args, kwargs )
        if unorderedCall is not None:
                self._debug( 'scenario: %s' % unorderedCall )
                return unorderedCall.result()

        return self._resultForOrderedCall( fakeObjectPath, args, kwargs )

    def _resultForOrderedCall( self, fakeObjectPath, args, kwargs ):
        if len( self._expected ) == 0:
                raise testixexception.ExpectationException( "unexpected call %s. Expected nothing" % self._formatActualCall( fakeObjectPath, args, kwargs ) )
        expected = self._expected.pop( 0 )
        self._verifyCallExpected( expected, fakeObjectPath, args, kwargs )
        result = expected.result()
        self._executeHooks()
        self._debug( 'scenario: %s' % expected )
        return result

    def _executeHooks( self ):
        while len( self._expected ) > 0 and isinstance( self._expected[ 0 ], hook.Hook ):
                currentHook = self._expected.pop( 0 )
                currentHook.execute()

    def _findUnorderedCall( self, fakeObjectPath, args, kwargs ):
        for call in self._unorderedExpectations:
                if call.fits( fakeObjectPath, args, kwargs ):
                        if not call.everlasting_():
                                self._unorderedExpectations.remove( call )
                        return call
        return None

    def _verifyCallExpected( self, expected, fakeObjectPath, args, kwargs ):
        if not expected.fits( fakeObjectPath, args, kwargs ):
                raise testixexception.ExpectationException( "unexpected call %s. Expected %s" % ( self._formatActualCall( fakeObjectPath, args, kwargs ), expected ) )

    def _formatActualCall( self, fakeObjectPath, args, kwargs ):
        argsString = ', '.join( [ pprint.pformat( arg ) for arg in args ] )
        if len( kwargs ) > 0:
                kwargsString = ', '.join( '%s = %s' % ( key, pprint.pformat( val ) ) for (key, val) in kwargs.items() )
                return '%s( %s, %s )' % ( fakeObjectPath, argsString, kwargsString )
        else:
                return '%s( %s )' % ( fakeObjectPath, argsString )

    @staticmethod
    def current():
        return Scenario._current

    def _performEndVerifications( self ):
        if len( self._expected ) > 0:
                raise testixexception.ExpectationException( "Scenario ended, but not all expectations were met. Pending expectations: %s" % self._expected )
        unorderedMortalExpectations = [ expectation for expectation in self._unorderedExpectations if not expectation.everlasting_() ]
        if len( unorderedMortalExpectations ) > 0:
                raise testixexception.ExpectationException( "Scenario ended, but not all expectations were met. There are still unordered pending expectations: %s" % unorderedMortalExpectations )

    def end( self ):
        if self._endingVerifications:
            self._performEndVerifications()
        Scenario._current = None

    def __lshift__( self, expectation ):
        self.addEvent( expectation )
        return self

def clearAllScenarios():
    Scenario._current = None

def current():
    return Scenario.current()
