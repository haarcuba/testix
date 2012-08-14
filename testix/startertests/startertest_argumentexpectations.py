from testix import scenario
from testix import exception
from testix import expectations
from testix import argumentexpectations
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
		STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( exception.ExpectationException, fakeObject, 10 )
		aScenario.end()

	def starter_test_ArgumentIsAFakeObjectWithPath( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		anotherFakeObject = fakeobject.FakeObject( 'another fake object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 	'some object', [ argumentexpectations.ArgumentIsAFakeObjectWithPath( 'another fake object' ) ], 
								'the result' ) <<\
			expectations.Call( 	'some object', [ argumentexpectations.ArgumentIsAFakeObjectWithPath( 'yet another' ) ], 
								'another result' )

		STS_ASSERT_EQUALS( fakeObject( anotherFakeObject ), 'the result' )
		STS_ASSERT_EQUALS( fakeObject( fakeobject.FakeObject( 'yet another' ) ), 'another result' )
		aScenario.end()

	def starter_test_IgnoreArgument( self ):
		fakeObject = fakeobject.FakeObject( 'some object' )
		aScenario = scenario.Scenario() <<\
			expectations.Call( 'some object', [ 10 ], 'first' ) <<\
			expectations.Call( 'some object', [ argumentexpectations.IgnoreArgument() ], 'second' )
		STS_ASSERT_EQUALS( fakeObject( 10 ), 'first' )
		STS_ASSERT_EQUALS( fakeObject( "this doens't matter" ), 'second' )
		aScenario.end()

StarterTestArgumentExpectations()
