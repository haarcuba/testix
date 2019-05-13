from testix import testixexception
from testix import hook
from testix import scenario_mocks
from testix import failhooks
from testix import call_formatter
import pprint
import sys

class Scenario( object ):
    _current = None

    def __init__( self, verbose = False ):
        if Scenario._current is not None:
            failhooks.error( "New scenario started before previous one ended" )
        self._verbose = verbose
        self._expected = []
        self._unorderedExpectations = []
        self._endingVerifications = True
        Scenario._current = self

    def __enter__( self ):
        return scenario_mocks.ScenarioMocks(self)

    def __exit__( self, exceptionType, exception, traceback ):
        if exceptionType is not None:
            self._endingVerifications = False
        self._end()

    def _debug( self, message ):
        if not self._verbose:
                return
        sys.stderr.write( f'SCENARIO: {message}\n' )

    def addEvent( self, event ):
        if isinstance( event, hook.Hook ):
                self._expected.append( event )
                return
        call = event
        self._expected.append( call )

    def resultFor( self, fakeObjectPath, * args, ** kwargs ):
        self._debug( f'resultFor: {fakeObjectPath}, {args}, {kwargs}' )
        unorderedCall = self._findUnorderedCall( fakeObjectPath, args, kwargs )
        if unorderedCall is not None:
            self._debug( f'found unordered call: {unorderedCall}' )
            return unorderedCall.result()

        return self._resultForOrderedCall( fakeObjectPath, args, kwargs )

    def _resultForOrderedCall( self, fakeObjectPath, args, kwargs ):
        self._debug( f'_resultForOrderedCall: {fakeObjectPath}, {args}, {kwargs}' )
        if len( self._expected ) == 0:
            failhooks.fail( testixexception.ExpectationException, f"unexpected call: {call_formatter.format( fakeObjectPath, args, kwargs )}\n"
                                                                   "Expected nothing" )
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
        self._debug( f'_verifyCallExpected: {expected}. actual={fakeObjectPath} args={args}, kwargs={kwargs}' )
        if not expected.fits( fakeObjectPath, args, kwargs ):
            failhooks.fail( testixexception.ExpectationException, 
                                  f"expected: {expected}\n"
                                  f"actual  : {call_formatter.format( fakeObjectPath, args, kwargs )}\n" )

    @staticmethod
    def current():
        return Scenario._current

    def _performEndVerifications( self ):
        if len( self._expected ) > 0:
            failhooks.fail( testixexception.ScenarioException, f"Scenario ended, but not all expectations were met. Pending expectations (ordered): {self._expected}" )
        mortalUnordered = [ expectation for expectation in self._unorderedExpectations if not expectation.everlasting_() ]
        if len( mortalUnordered ) > 0:
            failhooks.fail( testixexception.ScenarioException, f"Scenario ended, but not all expectations were met. Pending expectations (unordered): {mortalUnordered}" )

    def _end( self ):
        Scenario._current = None
        if self._endingVerifications:
            self._performEndVerifications()

    def unordered( self, call ):
        self._expected.remove( call )
        self._unorderedExpectations.append( call )

def clearAllScenarios():
    Scenario._current = None

def current():
    return Scenario.current()
