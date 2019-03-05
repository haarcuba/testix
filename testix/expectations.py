from testix import argumentexpectations

class Call:
    def __init__( self, fakeObjectPath, * arguments, ** kwargExpectations ):
        self._fakeObjectPath = fakeObjectPath
        self._argumentExpectations = [ self._expectation( arg ) for arg in arguments ]
        self._result = None
        self._kwargExpectations = { name: self._expectation( kwargExpectations[ name ] ) for name in kwargExpectations }
        self._unordered = False
        self._everlasting = False
        self._throwing = False

    def returns( self, result ):
        self._result = result
        return self

    def __rshift__( self, result ):
        self.returns( result )

    def throwing( self, exceptionFactory ):
        self._throwing = True
        self._exceptionFactory = exceptionFactory

    def unordered( self ):
        self._unordered = True
        assert not ( self._everlasting and ( not self._unordered ) )
        return self

    def everlasting( self ):
        self._everlasting = True
        assert not ( self._everlasting and ( not self._unordered ) )
        return self

    def _expectation( self, arg ):
        if isinstance( arg, argumentexpectations.ArgumentExpectation ):
            return arg
        defaultExpectation = argumentexpectations.ArgumentEquals
        return defaultExpectation( arg )

    def result( self ):
        if self._throwing:
            raise self._exceptionFactory()
        return self._result

    def __repr__( self ):
        argumentExpectationString = ', '.join( [ str( argExp ) for argExp in self._argumentExpectations ] )
        if len( self._kwargExpectations ) > 0:
            kwargsString = ', '.join( '%s = %s' % tupl for tupl in self._kwargExpectations.items() )
            return '%s( %s, %s )' % ( self._fakeObjectPath, argumentExpectationString, kwargsString )
        else:
            return '%s( %s )' % ( self._fakeObjectPath, argumentExpectationString )

    def fits( self, fakeObjectPath, args, kwargs ):
        if fakeObjectPath != self._fakeObjectPath:
            return False
        if not self._verifyArguments( args ):
            return False
        if not self._verifyKeywordArguments( kwargs ):
            return False
        return True

    def _verifyArguments( self, args ):
        args = list( args )
        argumentExpectations = list( self._argumentExpectations )
        if len( argumentExpectations ) != len( args ):
            return False
        while len( argumentExpectations ) > 0:
            argumentExpectation = argumentExpectations.pop( 0 )
            actualArgument = args.pop( 0 )
            if not argumentExpectation.ok( actualArgument ):
                return False
        return True

    def _verifyKeywordArguments( self, kwargs ):
        for name, argumentExpectation in self._kwargExpectations.items():
            if name not in kwargs:
                return False
            actualArgument = kwargs[ name ]
            if not argumentExpectation.ok( actualArgument ):
                return False
        if self._unexpectedKeyworkArgument( kwargs ):
            return False
        return True

    def _unexpectedKeyworkArgument( self, kwargs ):
        for name in kwargs:
            if name not in self._kwargExpectations:
                return True

    def unordered_( self ):
        return self._unordered

    def everlasting_( self ):
        return self._everlasting
