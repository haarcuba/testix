from testix import scenario
from testix import testixexception
from testix import expectations
from testix import argumentexpectations
from testix import saveargument
from testix import fakeobject
from testix.startertests import startertestcollection
from testix.startertests.asserts import *

class StarterTestArgumentExpectations( startertestcollection.StarterTestCollection ):
	def starter_test_ArgumentEquals( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 10 ], 'first' ) <<\
			expectations.Call( 'some object', [ 11 ], 'second' )
		STS_ASSERT_EQUALS( fakeObject( 10 ), 'first' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 10 )
		aScenario.end()

	def starter_test_ArgumentIsFakeObjectWithPath( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		anotherFakeObject = fakeobject.FakeObject( 'another fake object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 	'some object', [ argumentexpectations.ArgumentIsFakeObjectWithPath( 'another fake object' ) ], 
								'the result' ) <<\
			expectations.Call( 	'some object', [ argumentexpectations.ArgumentIsFakeObjectWithPath( 'yet another' ) ], 
								'another result' )

		STS_ASSERT_EQUALS( fakeObject( anotherFakeObject ), 'the result' )
		STS_ASSERT_EQUALS( fakeObject( fakeobject.FakeObject( 'yet another' ) ), 'another result' )
		aScenario.end()

	def starter_test_FakeObjectExpectation( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		fakeArgument = fakeobject.FakeObject( 'fake argument' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ fakeobject.FakeObject( 'fake argument' ) ], None )
		fakeObject( fakeArgument )
		aScenario.end()

	def starter_test_IgnoreArgument( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 10 ], 'first' ) <<\
			expectations.Call( 'some object', [ argumentexpectations.IgnoreArgument() ], 'second' )
		STS_ASSERT_EQUALS( fakeObject( 10 ), 'first' )
		STS_ASSERT_EQUALS( fakeObject( "this doens't matter" ), 'second' )
		aScenario.end()

	def starter_test_KeywordArguments( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 10 ], 'first', kwargExpectations = { 'name': 'Lancelot' } ) <<\
			expectations.Call( 'some object', [ 11 ], 'second', kwargExpectations = { 'name': 'Galahad' } )
		STS_ASSERT_EQUALS( fakeObject( 10, name = 'Lancelot' ), 'first' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 11, name = 'not Galahad'  )
		aScenario.end()

	def starter_test_KeywordArgumentsExpected_NoneGiven( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 11 ], 'result', kwargExpectations = { 'name': 'Galahad' } )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 11 )
		aScenario.end()

	def starter_test_KeywordArgumentsForThrowingCall( self ):
		class MyException( Exception ): pass

		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.ThrowingCall( 'some object', [ 'no kwargs will violate expectation' ], MyException, kwargExpectations = { 'name': 'Galahad' } )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 'no kwargs will violate expectation' )
		aScenario.end()

		aScenario = scenario.Scenario() <<\
			expectations.ThrowingCall( 'some object', [ 11 ], MyException, kwargExpectations = { 'name': 'Galahad' } )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( MyException, fakeObject, 11, name = 'Galahad' )
		aScenario.end()

	def starter_test_Bugfix_NumberOfArguments_can_be_different_FromExpectedNumberOfArguments( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ argumentexpectations.IgnoreArgument(), argumentexpectations.IgnoreArgument() ], 'result' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 1, 2, 3 )
		aScenario.end()

	def starter_test_SaveArgument( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 'first', saveargument.SaveArgument( 'second' ) ], None )
		fakeObject( 'first', 'value of second argument' )
		aScenario.end()
		STS_ASSERT_EQUALS( saveargument.saved()[ 'second' ], 'value of second argument' )

	def starter_test_SaveArgument_With_KeyworkArgument( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 'first'  ], None, kwargExpectations = { 'god': saveargument.SaveArgument( 'god' ) } )
		fakeObject( 'first', god = 'Zeus' )
		aScenario.end()
		STS_ASSERT_EQUALS( saveargument.saved()[ 'god' ], 'Zeus' )

	def starter_test_Bugfix_UnexpectedKeywordArgument( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 11 ], 'some result', kwargExpectations = { 'name': 'Lancelot' } )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 11, name = 'Lancelot', maidenName = 'Sarah' )
		aScenario.end()

	def starter_test_ArgumentIs( self ):
		class X( object ):
			def __eq__( self, other ):
				return True

		x = X()
		y = X()
		STS_ASSERT_EQUALS( x, y )
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ argumentexpectations.ArgumentIs( x ) ], 'first' ) <<\
			expectations.Call( 'some object', [ argumentexpectations.ArgumentIs( y ) ], 'second' )
		STS_ASSERT_EQUALS( fakeObject( x ), 'first' )
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, x )
		aScenario.end()

StarterTestArgumentExpectations()
