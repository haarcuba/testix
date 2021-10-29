from testix import testixexception
from testix import hook
from testix import scenario_mocks
from testix import failhooks
from testix import call_formatter
import traceback
import pprint
import sys

class Scenario( object ):
    _current = None
    init_hook = lambda: None

    def __init__( self, title='', *, verbose = False ):
        Scenario.init_hook()
        if Scenario._current is not None:
            failhooks.error( "New scenario started before previous one ended" )
        self.__title = title
        self.__verbose = verbose
        self.__expected = []
        self.__unorderedExpectations = []
        self.__endingVerifications = True
        Scenario._current = self

    def __enter__( self ):
        return scenario_mocks.ScenarioMocks(self)

    def __exit__( self, exceptionType, exception, traceback ):
        if exceptionType is not None:
            self.__endingVerifications = False
        self.__end()

    def __debug( self, message ):
        if not self.__verbose:
                return
        sys.stderr.write( f'SCENARIO: {message}\n' )

    def addEvent( self, event ):
        if isinstance( event, hook.Hook ):
                self.__expected.append( event )
                return
        call = event
        self.__expected.append( call )

    def resultFor( self, fakeObjectPath, * args, ** kwargs ):
        self.__debug( f'resultFor: {fakeObjectPath}, {args}, {kwargs}' )
        unorderedCall = self.__findUnorderedCall( fakeObjectPath, args, kwargs )
        if unorderedCall is not None:
            self.__debug( f'found unordered call: {unorderedCall}' )
            return unorderedCall.result()

        return self.__resultForOrderedCall( fakeObjectPath, args, kwargs )

    def __resultForOrderedCall( self, fakeObjectPath, args, kwargs ):
        self.__debug( f'_resultForOrderedCall: {fakeObjectPath}, {args}, {kwargs}' )
        if len( self.__expected ) == 0:
            message = self.__effective_title()
            message += f"unexpected call: {call_formatter.format( fakeObjectPath, args, kwargs )}\n"
            message += "Expected nothing" 
            failhooks.fail( testixexception.ExpectationException, message )
        expected = self.__expected.pop( 0 )
        self.__verifyCallExpected( expected, fakeObjectPath, args, kwargs )
        result = expected.result()
        self.__executeHooks()
        self.__debug(f'scenario: {expected} >> {result}')
        return result

    def __executeHooks( self ):
        while len( self.__expected ) > 0 and isinstance( self.__expected[ 0 ], hook.Hook ):
                currentHook = self.__expected.pop( 0 )
                currentHook.execute()

    def __findUnorderedCall( self, fakeObjectPath, args, kwargs ):
        for call in self.__unorderedExpectations:
            if call.fits( fakeObjectPath, args, kwargs ):
                    if not call.everlasting_():
                            self.__unorderedExpectations.remove( call )
                    return call
        return None

    def __effective_title(self):
        if self.__title != '':
            return f'=== Scenario "{self.__title}" ===\n'
        else:
            return f'=== Scenario (no title) ===\n'

    def __verifyCallExpected( self, expected, fakeObjectPath, args, kwargs ):
        self.__debug( f'_verifyCallExpected: {expected}. actual={fakeObjectPath} args={args}, kwargs={kwargs}' )
        if not expected.fits( fakeObjectPath, args, kwargs ):
            message = self.__effective_title()
            message += f" expected: {expected}\n"
            message += f" actual  : {call_formatter.format( fakeObjectPath, args, kwargs )}\n"
            message += '=== OFFENDING LINE ===\n'
            message += " " + call_formatter.caller_context() + '\n'
            message += f'=== FURTHER EXPECTATIONS (showing at most 10 out of {len(self.__expected)}) ===\n'
            for expectation in self.__expected[:10]:
                message += f' {expectation}\n'
            message += '=== END ===\n'


            failhooks.fail( testixexception.ExpectationException, message )

    @staticmethod
    def current():
        return Scenario._current

    def __performEndVerifications( self ):
        if len( self.__expected ) > 0:
            failhooks.fail( testixexception.ScenarioException, f"Scenario ended, but not all expectations were met. Pending expectations (ordered): {self.__expected}" )
        mortalUnordered = [ expectation for expectation in self.__unorderedExpectations if not expectation.everlasting_() ]
        if len( mortalUnordered ) > 0:
            failhooks.fail( testixexception.ScenarioException, f"Scenario ended, but not all expectations were met. Pending expectations (unordered): {mortalUnordered}" )

    def __end( self ):
        Scenario._current = None
        if self.__endingVerifications:
            self.__performEndVerifications()

    def unordered( self, call ):
        self.__expected.remove( call )
        self.__unorderedExpectations.append( call )

def clearAllScenarios():
    Scenario._current = None

def current():
    return Scenario.current()
