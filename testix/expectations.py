from testix import argumentexpectations

class Call( object ):
	def __init__( self, fakeObjectPath, arguments, result, unordered = False, everlasting = False, kwargExpectations = None ):
		assert not ( everlasting and ( not unordered ) )
		if kwargExpectations == None:
			kwargExpectations = {}
		self._fakeObjectPath = fakeObjectPath
		self._argumentExpectations = [ self._expectation( arg ) for arg in arguments ]
		self._result = result
		self._kwargExpectations = { name: self._expectation( kwargExpectations[ name ] ) for name in kwargExpectations }
		self._unordered = unordered
		self._everlasting = everlasting

	def _expectation( self, arg ):
		if isinstance( arg, argumentexpectations.ArgumentExpectation ):
			return arg
		defaultExpectation = argumentexpectations.ArgumentEquals
		return defaultExpectation( arg )
	
	def result( self ):
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

	def unordered( self ):
		return self._unordered

	def everlasting( self ):
		return self._everlasting

class ThrowingCall( Call ):
	def __init__( self, fakeObjectPath, arguments, exceptionType, kwargExpectations = None ):
		self._exceptionType = exceptionType
		Call.__init__( self, fakeObjectPath, arguments, None, kwargExpectations = kwargExpectations )

	def result( self ):
		Call.result( self )
		raise self._exceptionType()
