from testix import argumentexpectations
from testix import scenario
from testix import call_formatter
from testix import DSL
from testix import modifiers
from testix import context_wrapper
import testix.context_wrapper.synchronous
import contextlib
import copy

def _async(result):
    async def _awaitable():
        return result

    return _awaitable()

class Call:
    def __init__( self, fakeObjectPath, * arguments, ** kwargExpectations ):
        self.__fakeObjectPath = fakeObjectPath
        self.__argumentExpectations = [ self.__expectation( arg ) for arg in arguments ]
        self.__result = None
        self.__kwargExpectations = { name: self.__expectation( kwargExpectations[ name ] ) for name in kwargExpectations }
        self.__unordered = False
        self.__everlasting = False
        self.__throwing = False
        self.__is_context = False
        self.__context_wrapper = context_wrapper.synchronous.Synchronous(self)
        self.__modifiers = modifiers.Modifiers()

    @property
    def context_wrapper(self):
        return self.__context_wrapper

    def returns( self, result ):
        if self.__modifiers.is_context:
            self.__context_wrapper.set_entry_value(result)
            result = self.__context_wrapper
        if self.__modifiers.awaitable:
            self.__result = _async(result)
        else:
            self.__result = result
        return self

    def modify(self, modifiers):
        self.__modifiers = copy.copy(modifiers)
        self.__force_context_wrapper_behaviour()

    def __force_context_wrapper_behaviour(self):
        self.returns(None)

    def __rshift__( self, result ):
        if type(result) is DSL.Throwing:
            self.throwing(result.exceptionFactory)
        else:
            self.returns( result )

    def throwing( self, exceptionFactory ):
        self.__throwing = True
        self.__exceptionFactory = exceptionFactory
        return self

    def unordered( self ):
        scenario.current().unordered( self )
        self.__unordered = True
        return self

    def everlasting( self ):
        self.__everlasting = True
        assert self.__unordered, "call cannot be everlasting but not unordered"
        return self

    def __expectation( self, arg ):
        if isinstance( arg, argumentexpectations.ArgumentExpectation ):
            return arg
        defaultExpectation = argumentexpectations.ArgumentEquals
        return defaultExpectation( arg )

    def result( self ):
        if self.__throwing:
            raise self.__exceptionFactory()
        return self.__result

    def __repr__( self ):
        return call_formatter.format( self.__fakeObjectPath, self.__argumentExpectations, self.__kwargExpectations )

    def fits( self, fakeObjectPath, args, kwargs ):
        if fakeObjectPath != self.__fakeObjectPath:
            return False
        if self.__ignoreCallDetails():
            return True
        if not self.__verifyArguments( args ):
            return False
        if not self.__verifyKeywordArguments( kwargs ):
            return False
        return True

    def __ignoreCallDetails(self):
        argumentExpectations = list( self.__argumentExpectations )
        if len(argumentExpectations) == 0:
            return False
        first = argumentExpectations[0]
        return type(first) is argumentexpectations.IgnoreCallDetails

    def __verifyArguments( self, args ):
        args = list( args )
        argumentExpectations = list( self.__argumentExpectations )
        if len( argumentExpectations ) != len( args ):
            return False
        while len( argumentExpectations ) > 0:
            argumentExpectation = argumentExpectations.pop( 0 )
            actualArgument = args.pop( 0 )
            if not argumentExpectation.ok( actualArgument ):
                return False
        return True

    def __verifyKeywordArguments( self, kwargs ):
        for name, argumentExpectation in self.__kwargExpectations.items():
            if name not in kwargs:
                return False
            actualArgument = kwargs[ name ]
            if not argumentExpectation.ok( actualArgument ):
                return False
        if self.__unexpectedKeyworkArgument( kwargs ):
            return False
        return True

    def __unexpectedKeyworkArgument( self, kwargs ):
        for name in kwargs:
            if name not in self.__kwargExpectations:
                return True

    def unordered_( self ):
        return self.__unordered

    def everlasting_( self ):
        return self.__everlasting
