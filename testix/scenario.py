from testix import testixexception
from testix import hook
from testix import scenario_mocks
import pprint
import sys

class Scenario( object ):
    _current = None

    def __init__( self, verbose = False ):
        if Scenario._current is not None:
                raise testixexception.TestixException( "New scenario started before previous one ended" )
        self._verbose = verbose
        self._expected = []
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
        if len( self._orderedExpectationsView() ) == 0:
                raise testixexception.ExpectationException( "unexpected call %s. Expected nothing" % self._formatActualCall( fakeObjectPath, args, kwargs ) )
        expected = self._findOrderedCall( fakeObjectPath, args, kwargs )
        self._expected.remove( expected )
        self._verifyCallExpected( expected, fakeObjectPath, args, kwargs )
        result = expected.result()
        self._executeHooks()
        self._debug( 'scenario: %s' % expected )
        return result

    def _executeHooks( self ):
        while len( self._expected ) > 0 and isinstance( self._expected[ 0 ], hook.Hook ):
                currentHook = self._expected.pop( 0 )
                currentHook.execute()

    def _unorderedExpectationsView( self ):
        result = []
        for expectation in self._expected:
            if isinstance( expectation, hook.Hook ):
                continue
            if not expectation.unordered_():
                continue
            result.append( expectation )

        return result

    def _orderedExpectationsView( self ):
        result = []
        for expectation in self._expected:
            if isinstance( expectation, hook.Hook ):
                continue
            if expectation.unordered_():
                continue
            result.append( expectation )

        return result

    def _pendingExpectations( self ):
        result = []
        for expectation in self._expected:
            if isinstance( expectation, hook.Hook ):
                continue
            if expectation.everlasting_():
                continue
            result.append( expectation )

        return result

    def _findUnorderedCall( self, fakeObjectPath, args, kwargs ):
        for call in self._unorderedExpectationsView():
            if call.fits( fakeObjectPath, args, kwargs ):
                    if not call.everlasting_():
                            self._expected.remove( call )
                    return call
        return None

    def _findOrderedCall( self, fakeObjectPath, args, kwargs ):
        call, *_ = self._orderedExpectationsView()
        return call

    def _verifyCallExpected( self, expected, fakeObjectPath, args, kwargs ):
        self._debug( f'_verifyCallExpected: {expected}. actual={fakeObjectPath} args={args}, kwargs={kwargs}' )
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
        if len( self._pendingExpectations() ) > 0:
                raise testixexception.ScenarioException( "Scenario ended, but not all expectations were met. Pending expectations: %s" % self._expected )

    def _end( self ):
        Scenario._current = None
        if self._endingVerifications:
            self._performEndVerifications()

def clearAllScenarios():
    Scenario._current = None

def current():
    return Scenario.current()
