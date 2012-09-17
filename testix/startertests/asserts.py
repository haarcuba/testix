from testix import fakeobject

class StarterTestAssertionFailed( Exception ): pass

def STS_ASSERT( condition ):
	if not condition:
		raise StarterTestAssertionFailed( "the condition was false" )

def STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exceptionType, call, * args, ** kwargs ):
	try:
		call( * args, ** kwargs )
	except exceptionType:
		pass
	else:
		raise StarterTestAssertionFailed( "call '%s' should have thrown an exception of type '%s', but it did not" % ( call, exceptionType ) )

def STS_ASSERT_EQUALS( a, b ):
	if not ( a == b ):
		raise StarterTestAssertionFailed( "%s != %s" % ( a, b ) )

def STS_ASSERT_IS_FAKE_OBJECT( candidate, fakeObjectPath ):
	if candidate is not fakeobject.FakeObject( fakeObjectPath ):
		raise StarterTestAssertionFailed( 'got "%s", expected "%s"' % ( candidate, fakeObjectPath ) )

def STS_ASSERT_DOES_NOT_THROW( call, * args, ** kwargs ):
	try:
		call( * args, ** kwargs )
	except:
		raise StarterTestAssertionFailed( "call %s shouldn't have thrown an exception, but it did" )
