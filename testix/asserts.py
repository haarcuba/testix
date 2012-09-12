import testix.exception
import pprint

class TestAssertionFailed( testix.exception.Exception ): pass

def TS_ASSERT( condition ):
	if not condition:
		raise TestAssertionFailed()

class TestEqualsFailed( TestAssertionFailed ):
	def __init__( self, actual, expected ):
		TestAssertionFailed.__init__( self, '%s (actual) does not equal %s (expected)' % ( actual, expected ) )
def TS_ASSERT_EQUALS( a, b ):
	condition = ( a == b )
	if not condition:
		raise TestEqualsFailed( a, b )

class TestSetsEqualFailed( TestAssertionFailed ):
	def __init__( self, actualSet, expectedSet ):
		actualString = pprint.pformat( actualSet )
		expectedString = pprint.pformat( expectedSet )
		TestAssertionFailed.__init__( self, '%s (actual) does not equal %s (expected)' % ( actualString, expectedString ) )
def TS_ASSERT_SETS_EQUAL( actual, expected ):
	actualSet = set( actual )
	expectedSet = set( expected )
	if not actualSet == expectedSet:
		raise TestSetsEqualFailed( actualSet, expectedSet )

def TS_ASSERT_LESS_THAN( a, b ):
	condition = ( a < b )
	if not condition:
		raise TestAssertionFailed( '%s is not less than %s' % ( a, b ) )

class TestAssertThrowsFailed( TestAssertionFailed ):
	def __init__( self, call ):
		TestAssertionFailed.__init__( self, "function '%s' should have thrown an exception, but it didn't" % call )
def TS_ASSERT_THROWS( call, * args, ** kwargs ):
	try:
		call( * args, ** kwargs )
	except testix.exception.Exception:
		raise
	except:
		pass
	else:
		raise TestAssertThrowsFailed( call )

class TestAssertThrowsSpecificExceptionFailed( TestAssertionFailed ):
	def __init__( self, exceptionType, call, actualExceptionCaught = None ):
		if actualExceptionCaught is not None:
			TestAssertionFailed.__init__( self, "function '%s' should have thrown a '%s', it threw '%s' instead" % ( call, exceptionType,actualExceptionCaught ) )
		else:
			TestAssertionFailed.__init__( self, "function '%s' should have thrown a '%s', but it didn't" % ( call, exceptionType ) )
def TS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exceptionType, call, * args, ** kwargs ):
	try:
		call( * args, ** kwargs )
	except exceptionType:
		pass
	except testix.exception.Exception:
		raise
	except Exception, e:
		raise TestAssertThrowsSpecificExceptionFailed( exceptionType, call, e )
	else:
		raise TestAssertThrowsSpecificExceptionFailed( exceptionType, call )
