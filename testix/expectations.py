from testix import argumentexpectations

class Call( object ):
	def __init__( self, fakeObjectPath, arguments, result ):
		self._fakeObjectPath = fakeObjectPath
		self._argumentExpectations = [ self._expectation( arg ) for arg in arguments ]
		self._result = result

	def _expectation( self, arg ):
		if isinstance( arg, argumentexpectations.ArgumentExpectation ):
			return arg
		defaultExpectation = argumentexpectations.ArgumentEquals
		return defaultExpectation( arg )

	def result( self ):
		return self._result

	def __repr__( self ):
		return 'Call( "%s", %s, %s )' % ( self._fakeObjectPath, self._argumentExpectations, self._result )

	def fits( self, fakeObjectPath, args ):
		if fakeObjectPath != self._fakeObjectPath:
			return False

		args = list( args )
		argumentExpectations = list( self._argumentExpectations )
		while len( argumentExpectations ) > 0:
			argumentExpectation = argumentExpectations.pop( 0 )
			actualArgument = args.pop( 0 )
			if not argumentExpectation.ok( actualArgument ):
				return False
		return True

class ThrowingCall( Call ):
	def __init__( self, fakeObjectPath, arguments, exceptionType ):
		self._exceptionType = exceptionType
		Call.__init__( self, fakeObjectPath, arguments, None )

	def result( self ):
		raise self._exceptionType()
