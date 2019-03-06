import pytest
import hypothesis
import hypothesis.strategies as strategies
from testix import scenario
from testix import testixexception
from testix import expectations
from testix import hook
from testix import fakeobject

class TestScenario:
    def test_EmptyScenario( self ):
        with scenario.Scenario() as s:
            pass

    def test_OnlyOneScenarioMayExistAtAnyOneTime( self ):
        with scenario.Scenario() as s:
            with pytest.raises( testixexception.TestixException ):
                scenario.Scenario()

    def test_TwoScenariosOneAfterTheOther( self ):
        with scenario.Scenario() as s:
            pass
        with scenario.Scenario() as s:
            pass

    @hypothesis.given(A=strategies.integers(),B=strategies.integers())
    def test_CallExpectationReturnsFakeValue(self, A, B):
        with scenario.Scenario() as s:
            s << expectations.Call( 'some_object', A ).returns( B )
            fakeObject = fakeobject.FakeObject( 'some_object' )
            assert fakeObject( A ) == B

    @hypothesis.given(A=strategies.integers(),B=strategies.integers(),C=strategies.integers(),D=strategies.integers(),E=strategies.integers())
    def test_TwoFakeCallsGetCorrectValues(self, A, B, C, D, E):
        with scenario.Scenario() as s:
            s.some_object( A ) >> B
            s.another_object( C, D ) >> E
            some_object = fakeobject.FakeObject( 'some_object' )
            another_object = fakeobject.FakeObject( 'another_object' )
            assert some_object( A ) == B
            assert another_object( C, D ) == E

    def test_TwoFakeCalls_MustBeInOrder( self ):
        class PreventScenarioEndVerifications(Exception): pass
        with pytest.raises(PreventScenarioEndVerifications):
            with scenario.Scenario() as s:
                s.some_object( 10 ).returns( 15 )
                s.another_object( 20, 50 ).returns( 30 )
                some_object = fakeobject.FakeObject( 'some_object' )
                another_object = fakeobject.FakeObject( 'another_object' )
                with pytest.raises( testixexception.ExpectationException ):
                    another_object( 20, 50 )

                raise PreventScenarioEndVerifications()

    def test_Four_FakeCalls_MustBeInOrder( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ) >> 15
            s.another_object( 20, 50 ).returns( 30 )
            s.some_object( 'x' ).returns( 'y' )
            s.another_object( 'X', 'Y' ) >> 'Z'
            some_object = fakeobject.FakeObject( 'some_object' )
            another_object = fakeobject.FakeObject( 'another_object' )
            assert some_object( 10 ) == 15
            assert another_object( 20, 50 ) == 30
            assert some_object( 'x' ) == 'y'
            assert another_object( 'X', 'Y' ) == 'Z'

    def test_ScenarioEndsPrematurely( self ):
        with pytest.raises( testixexception.ScenarioException ):
            with scenario.Scenario() as s:
                s.some_object( 10 ).returns( 15 )
                s.another_object( 20, 50 ).returns( 30 )
                some_object = fakeobject.FakeObject( 'some_object' )
                another_object = fakeobject.FakeObject( 'another_object' )
                assert some_object( 10 ) == 15

    @pytest.mark.skip(reason='will fix later')
    def test_bugfix_ScenarioEndsPrematurely_With_UnorderedCalls( self ):
        with pytest.raises( testixexception.ScenarioException ):
            with scenario.Scenario() as s:
                s.some_object( 10 ).returns( 15 )
                s.another_object( 20, 50 ).returns( 30 ).unordered()
                some_object = fakeobject.FakeObject( 'some_object' )
                assert some_object( 10 ) == 15

    def test_CallParametersDontMatch( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).returns( 15 )
            some_object = fakeobject.FakeObject( 'some_object' )
            with pytest.raises( testixexception.ExpectationException ):
                some_object( 1024 )

    def test_ShiftLeftOperator( self ):
        with scenario.Scenario() as s:
            s <<\
                expectations.Call( 'some_object', 10 ).returns( 15 ) <<\
                expectations.Call( 'some_object', 15 ).returns( 30 )
            some_object = fakeobject.FakeObject( 'some_object' )
            assert some_object( 10 ) == 15
            assert some_object( 15 ) == 30

    def test_ThrowingCallExpectation( self ):
        class MyException( Exception ): pass

        with scenario.Scenario() as s:
            s.some_object( 10 ).throwing( MyException )
            some_object = fakeobject.FakeObject( 'some_object' )
            with pytest.raises( MyException ):
                some_object( 10 )

    @pytest.mark.skip(reason='will fix later')
    @hypothesis.given( values=strategies.permutations( [ 10, 11 ] ) )
    def test_UnorderedExpectation( self, values ):
        print( values )
        with scenario.Scenario() as s:
            s.some_object( 10 ).unordered()
            s.some_object( 11 ).unordered()

            some_object = fakeobject.FakeObject( 'some_object' )
            some_object( values[ 0 ] )
            some_object( values[ 1 ] )

    @pytest.mark.skip(reason='will fix later')
    def test_UnorderedExpectationsRunOut( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).unordered()
            s.some_object( 11 ).unordered()

            some_object = fakeobject.FakeObject( 'some_object' )
            some_object( 11 )
            some_object( 10 )
            with pytest.raises( testixexception.ScenarioException ):
                some_object( 11 )

    @pytest.mark.skip(reason='will fix later')
    def test_EverlastingCall( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some_object', 10 ).unordered().everlasting() << \
                    expectations.Call( 'some_object', 11 ).unordered().everlasting()

            fakeObject = fakeobject.FakeObject( 'some_object' )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 10 )
            fakeObject( 11 )
            fakeObject( 11 )

    @pytest.mark.skip(reason='will fix later')
    def test_Everlasting_Unorderd_and_Regular_Calls( self ):
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

    @pytest.mark.skip(reason='will fix later')
    def test_Everlasting_Calls_Have_ArgumentExpectations( self ):
        with scenario.Scenario() as aScenario:
            aScenario <<\
                    expectations.Call( 'some_object', 10 ).returns( 'ten' ).unordered().everlasting()

            someObject = fakeobject.FakeObject( 'some_object' )
            STS_ASSERT_EQUALS( someObject( 10 ), 'ten' )
            STS_ASSERT_THROWS_SPECIFIC_EXCEPTION( testixexception.TestixException, someObject, 11 )

    def test_Hooks( self ):
        func1Calls = []
        def func1( * a, **k ):
                func1Calls.append( ( a, k ) )

        with scenario.Scenario() as s:
            s.some_object( 10 )
            s << hook.Hook( func1, 10, 20, name = 'Moshe' )
            s << hook.Hook( func1, 70, 80, name = 'Avraham' )
            s.some_object( 11 )
            s << hook.Hook( func1, 11, 21, name = 'Haim' )

            some_object = fakeobject.FakeObject( 'some_object' )
            some_object( 10 )
            assert len( func1Calls ) == 2
            assert func1Calls[ 0 ] == ( ( 10, 20 ), { 'name': 'Moshe' } )
            assert func1Calls[ 1 ] == ( ( 70, 80 ), { 'name': 'Avraham' } )
            some_object( 11 )
            assert len( func1Calls ) == 3
            func1Calls[ 2 ] == ( 11, 21 ), { 'name': 'Haim' }
