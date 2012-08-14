from testix import scenario
from testix import exception
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
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.Exception, scenario.Scenario )

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
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, fakeObject2, 20, 50 )

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
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, aScenario.end )

	def starter_test_CallParametersDontMatch( self ):
		aScenario = scenario.Scenario()
		aScenario.addCall( expectations.Call( 'some object', [ 10 ], 15 ) )
		fakeObject1 = fakeobject.FakeObject( 'some object' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, fakeObject1, 1024 )

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
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, testix.asserts.TS_ASSERT_THROWS_SPECIFIC_EXCEPTION, MyException, fakeObject, unexpectedArgumentValue )
		aScenario.end()

	def starter_test_Bugfix_AssertThrows_DoesNot_Block_TestAssertionFailures( self ):
		class MyException( Exception ): pass

		aScenario = scenario.Scenario()
		aScenario <<\
			expectations.ThrowingCall( 'some object', [ 10 ], MyException )
		fakeObject = fakeobject.FakeObject( 'some object' )
		unexpectedArgumentValue = 11
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, testix.asserts.TS_ASSERT_THROWS, fakeObject, unexpectedArgumentValue )
		aScenario.end()

StarterTestScenario()
