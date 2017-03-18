from testix import scenario
from testix import testixexception
from testix import expectations
from testix import hook
from startertests.asserts import *
from testix import fakeobject
from startertests import startertestcollection

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
        with scenario.Scenario() as aScenario:
            aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
            fakeObject = fakeobject.FakeObject( 'some object' )
            result = fakeObject( 10 )
            STS_ASSERT_EQUALS( result, 15 )
            aScenario.end()

    def starter_test_TwoFakeCallsGetCorrectValues( self ):
        with scenario.Scenario() as aScenario:
            aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
            aScenario.addEvent( expectations.Call( 'another object', 20, 50 ).returns( 30 ) )
            fakeObject1 = fakeobject.FakeObject( 'some object' )
            fakeObject2 = fakeobject.FakeObject( 'another object' )
            STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
            STS_ASSERT_EQUALS( fakeObject2( 20, 50 ), 30 )

    def starter_test_TwoFakeCalls_MustBeInOrder( self ):
        aScenario = scenario.Scenario()
        aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
        aScenario.addEvent( expectations.Call( 'another object', 20, 50 ).returns( 30 ) )
        fakeObject1 = fakeobject.FakeObject( 'some object' )
        fakeObject2 = fakeobject.FakeObject( 'another object' )
        STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject2, 20, 50 )

    def starter_test_Four_FakeCalls_MustBeInOrder( self ):
        with scenario.Scenario() as aScenario:
            aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
            aScenario.addEvent( expectations.Call( 'another object', 20, 50 ).returns( 30 ) )
            aScenario.addEvent( expectations.Call( 'some object', 'x' ).returns( 'y' ) )
            aScenario.addEvent( expectations.Call( 'another object', 'X', 'Y' ).returns( 'Z' ) )
            fakeObject1 = fakeobject.FakeObject( 'some object' )
            fakeObject2 = fakeobject.FakeObject( 'another object' )
            STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
            STS_ASSERT_EQUALS( fakeObject2( 20, 50 ), 30 )
            STS_ASSERT_EQUALS( fakeObject1( 'x' ), 'y' )
            STS_ASSERT_EQUALS( fakeObject2( 'X', 'Y' ), 'Z' )

    def starter_test_ScenarioEndsPrematurely( self ):
        aScenario = scenario.Scenario()
        aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
        aScenario.addEvent( expectations.Call( 'another object', 20, 50 ).returns( 30 ) )
        fakeObject1 = fakeobject.FakeObject( 'some object' )
        fakeObject2 = fakeobject.FakeObject( 'another object' )
        STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
        STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, aScenario.end )

    def starter_test_bugfix_ScenarioEndsPrematurely_With_UnorderedCalls( self ):
        aScenario = scenario.Scenario()
        aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
        aScenario.addEvent( expectations.Call( 'another object', 20, 50 ).returns( 30 ).unordered() )
        fakeObject1 = fakeobject.FakeObject( 'some object' )
        fakeObject2 = fakeobject.FakeObject( 'another object' )
        STS_ASSERT_EQUALS( fakeObject1( 10 ), 15 )
        STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, aScenario.end )

    def starter_test_CallParametersDontMatch( self ):
        aScenario = scenario.Scenario()
        aScenario.addEvent( expectations.Call( 'some object', 10 ).returns( 15 ) )
        fakeObject1 = fakeobject.FakeObject( 'some object' )
        STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject1, 1024 )

    def tearDown( self ):
        scenario.clearAllScenarios()

    def starter_test_ShiftLeftOperator( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).returns( 15 ) <<\
                    expectations.Call( 'some object', 15 ).returns( 30 )
            fakeObject = fakeobject.FakeObject( 'some object' )
            STS_ASSERT_EQUALS( fakeObject( 10 ), 15 )
            STS_ASSERT_EQUALS( fakeObject( 15 ), 30 )

    def starter_test_ThrowingCallExpectation( self ):
        class MyException( Exception ): pass

        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.ThrowingCall( MyException, 'some object', 10 )
            fakeObject = fakeobject.FakeObject( 'some object' )
            STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( MyException, fakeObject, 10 )

    def starter_test_UnorderedExpectation( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).unordered() << \
                    expectations.Call( 'some object', 11 ).unordered()

            fakeObject = fakeobject.FakeObject( 'some object' )
            fakeObject( 10 )
            fakeObject( 11 )

        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).unordered() << \
                    expectations.Call( 'some object', 11 ).unordered()

            fakeObject = fakeobject.FakeObject( 'some object' )
            fakeObject( 11 )
            fakeObject( 10 )

    def starter_test_UnorderedExpectationsRunOut( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).unordered() << \
                    expectations.Call( 'some object', 11 ).unordered()

            fakeObject = fakeobject.FakeObject( 'some object' )
            fakeObject( 10 )
            fakeObject( 11 )
            STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.ExpectationException, fakeObject, 11 )

    def starter_test_EverlastingCall( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).unordered().everlasting() << \
                    expectations.Call( 'some object', 11 ).unordered().everlasting()

            fakeObject = fakeobject.FakeObject( 'some object' )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 11 )
            fakeObject( 11 )

    def starter_test_Everlasting_Unorderd_and_Regular_Calls( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'everlasting', 10 ).returns( 'ten' ).unordered().everlasting() << \
                    expectations.Call( 'everlasting', 11 ).returns( 'eleven' ).unordered().everlasting() << \
                    expectations.Call( 'unordered', 20 ).returns( 'twenty' ).unordered() << \
                    expectations.Call( 'ordered', 1 ).returns( 'one' ) << \
                    expectations.Call( 'ordered', 2 ).returns( 'two' ) << \
                    expectations.Call( 'ordered', 3 ).returns( 'three' )

            ordered = fakeobject.FakeObject( 'ordered' )
            everlasting = fakeobject.FakeObject( 'everlasting' )
            unordered = fakeobject.FakeObject( 'unordered' )

            STS_ASSERT_EQUALS( everlasting( 10 ), 'ten' )
            STS_ASSERT_EQUALS( ordered( 1 ), 'one' )
            STS_ASSERT_EQUALS( ordered( 2 ), 'two' )
            STS_ASSERT_EQUALS( everlasting( 10 ), 'ten' )
            STS_ASSERT_EQUALS( everlasting( 11 ), 'eleven' )
            STS_ASSERT_EQUALS( everlasting( 11 ), 'eleven' )
            STS_ASSERT_EQUALS( everlasting( 10 ), 'ten' )
            STS_ASSERT_EQUALS( ordered( 3 ), 'three' )
            STS_ASSERT_EQUALS( everlasting( 11 ), 'eleven' )
            STS_ASSERT_EQUALS( everlasting( 10 ), 'ten' )
            STS_ASSERT_EQUALS( unordered( 20 ), 'twenty' )
            STS_ASSERT_EQUALS( everlasting( 10 ), 'ten' )

    def starter_test_Everlasting_Calls_Have_ArgumentExpectations( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some object', 10 ).returns( 'ten' ).unordered().everlasting()

            someObject = fakeobject.FakeObject( 'some object' )
            STS_ASSERT_EQUALS( someObject( 10 ), 'ten' )
            STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.TestixException, someObject, 11 )

    def starter_test_Hooks( self ):
        func1Calls = []
        def func1( * a, **k ):
                func1Calls.append( ( a, k ) )

        aScenario = scenario.Scenario()
        aScenario <<\
                expectations.Call( 'some object', 10 ) <<\
                hook.Hook( func1, 10, 20, name = 'Moshe' ) <<\
                hook.Hook( func1, 70, 80, name = 'Avraham' ) <<\
                expectations.Call( 'some object', 11 ) <<\
                hook.Hook( func1, 11, 21, name = 'Haim' )

        someObject = fakeobject.FakeObject( 'some object' )
        someObject( 10 )
        STS_ASSERT_EQUALS( len( func1Calls ), 2 )
        STS_ASSERT_EQUALS( func1Calls[ 0 ], ( ( 10, 20 ), { 'name': 'Moshe' } ) )
        STS_ASSERT_EQUALS( func1Calls[ 1 ], ( ( 70, 80 ), { 'name': 'Avraham' } ) )
        someObject( 11 )
        STS_ASSERT_EQUALS( len( func1Calls ), 3 )
        STS_ASSERT_EQUALS( func1Calls[ 2 ], ( ( 11, 21 ), { 'name': 'Haim' } ) )

StarterTestScenario()
