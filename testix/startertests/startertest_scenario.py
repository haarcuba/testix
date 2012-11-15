from testix import scenario
from testix import testixexception
from testix import expectations
import testix.asserts
from testix.startertests.asserts import *
from testix import fakeobject
from testix.startertests import startertestcollection

class StarterTestScenario( startertestcollection.StarterTestCollection ):
	def starter_test_EmptyScenario( self ):
		aScenario = scenario.Scenario()
		aScenario.end()

	def starter_test_OnlyOneScenarioMayExistAtAnyOneTime( self ):
		aScenario = scenario.Scenario()
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.TestixException, scenario.Scenario )

	def starter_test_TwoScenariosOneAfterTheOther( self ):
		aScenario = scenario.Scenario()
		aScenario.end()
		anotherScenario = scenario.Scenario()
		anotherScenario.end()

	def starter_test_CallExpectationReturnsFakeValue( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		fakeObject = fakeobject.FakeObject( 'some object' )
		result = fakeObject( 10 )
		STS_ASSERT_EQUALS( result, 15 )
		aScenario.end()

	def starter_test_TwoFakeCallsGetCorrectValues( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		aScenario.addCall( expectations.Call( 'another object', [ 20, 50 ], 30 ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		fakeObject2 = fakeobject.FakeObject( 'another object' )
		STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
		STS_ASSERT_EQUALS( fakeObject2( 20, 50 ), 30 )
		aScenario.end()

	def starter_test_TwoFakeCalls_MustBeInOrder( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		aScenario.addCall( expectations.Call( 'another object', [ 20, 50 ], 30 ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		fakeObject2 = fakeobject.FakeObject( 'another object' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject2, 20, 50 )

	def starter_test_Four_FakeCalls_MustBeInOrder( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		aScenario.addCall( expectations.Call( 'another object', [ 20, 50 ], 30 ) )
		aScenario.addCall( expectations.Call( 'some object', [ 'x' ], 'y' ) )
		aScenario.addCall( expectations.Call( 'another object', [ 'X', 'Y' ], 'Z' ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		fakeObject2 = fakeobject.FakeObject( 'another object' )
		STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
		STS_ASSERT_EQUALS( fakeObject2( 20, 50 ), 30 )
		STS_ASSERT_EQUALS( fakeObject1( 'x' ), 'y' )
		STS_ASSERT_EQUALS( fakeObject2( 'X', 'Y' ), 'Z' )
		aScenario.end()

	def starter_test_ScenarioEndsPrematurely( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		aScenario.addCall( expectations.Call( 'another object', [ 20, 50 ], 30 ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		fakeObject2 = fakeobject.FakeObject( 'another object' )
		STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, aScenario.end )

	def starter_test_CallParametersDontMatch( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject1, 1024 )

	def tearDown( self ):
		scenario.clearAllScenarios()

	def starter_test_ShiftLeftOperator( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'some object', [ 10 ], 15 ) <<\
			expectations.Call( 'some object', [ 15 ], 30 )
		fakeObject = fakeobject.FakeObject( 'some object' )
		STS_ASSERT_EQUALS( fakeObject( 10 ), 15 )
		STS_ASSERT_EQUALS( fakeObject( 15 ), 30 )
		aScenario.end()

	def starter_test_ThrowingCallExpectation( self ):
		class MyException( Exception ): pass

		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.ThrowingCall( 'some object', [ 10 ], MyException )
		fakeObject = fakeobject.FakeObject( 'some object' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( MyException, fakeObject, 10 )
		aScenario.end()

	def starter_test_Bugfix_AssertThrowsSpecific_DoesNot_Catch_TestSuiteExceptions( self ):
		class MyException( Exception ): pass

		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.ThrowingCall( 'some object', [ 10 ], MyException )
		fakeObject = fakeobject.FakeObject( 'some object' )
		unexpectedArgumentValue = 11
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, testix.asserts.TS_ASSERT_THROWS_SPECIFIC_EXCEPTION, MyException, fakeObject, unexpectedArgumentValue )
		aScenario.end()

	def starter_test_Bugfix_AssertThrows_DoesNot_Block_TestSuiteAssertionFailures( self ):
		class MyException( testix.asserts.TestAssertionFailed ): pass

		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.ThrowingCall( 'some object', [ 10 ], MyException )
		fakeObject = fakeobject.FakeObject( 'some object' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( MyException, testix.asserts.TS_ASSERT_THROWS, fakeObject, 10 )
		aScenario.end()

	def starter_test_Bugfix_TestSuiteExceptions_dont_get_caught_by_Except_Exception( self ):
		def catcher( call ):
			try:
				call()
			except( Exception ):
				pass

		class Thrower( object ):
			def __init__( self, exceptionType ):
				self._exceptionType = exceptionType
			def __call__( self ):
				raise self._exceptionType()

		STS_ASSERT_DOES_NOT_THROW( catcher, Thrower( Exception ) )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.TestixException, catcher, Thrower( testixexception.TestixException ) )

	def starter_test_UnorderedExpectation( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'some object', [ 10 ], None, unordered = True ) << \
			expectations.Call( 'some object', [ 11 ], None, unordered = True )

		fakeObject = fakeobject.FakeObject( 'some object' )
		fakeObject( 10 )
		fakeObject( 11 )
		aScenario.end()

		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'some object', [ 10 ], None, unordered = True ) << \
			expectations.Call( 'some object', [ 11 ], None, unordered = True )

		fakeObject = fakeobject.FakeObject( 'some object' )
		fakeObject( 11 )
		fakeObject( 10 )
		aScenario.end()

	def starter_test_UnorderedExpectationsRunOut( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'some object', [ 10 ], None, unordered = True ) << \
			expectations.Call( 'some object', [ 11 ], None, unordered = True )

		fakeObject = fakeobject.FakeObject( 'some object' )
		fakeObject( 10 )
		fakeObject( 11 )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 11 )
		aScenario.end()

	def starter_test_EverlastingCall( self ):
		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.Call( 'some object', [ 10 ], None, unordered = True, everlasting = True ) << \
			expectations.Call( 'some object', [ 11 ], None, unordered = True, everlasting = True )

		fakeObject = fakeobject.FakeObject( 'some object' )
		fakeObject( 10 )
		fakeObject( 10 )
		fakeObject( 10 )
		fakeObject( 10 )
		fakeObject( 11 )
		fakeObject( 11 )
		aScenario.end()

StarterTestScenario()
