import pytest
import hypothesis
import hypothesis.strategies as strategies
from testix import scenario
from testix import testixexception
from testix import expectations
from testix import hook
from testix import fake
from testix import fake_context
from testix import DSL

class TestScenario:
    def test_EmptyScenario( self ):
        with scenario.Scenario() as s:
            pass

    def test_OnlyOneScenarioMayExistAtAnyOneTime( self ):
        with scenario.Scenario() as s:
            with pytest.raises( testixexception.TestixError ):
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
            fakeObject = fake.Fake('some_object')
            assert fakeObject( A ) == B

    @hypothesis.given(A=strategies.integers(),B=strategies.integers(),C=strategies.integers(),D=strategies.integers(),E=strategies.integers())
    def test_TwoFakeCallsGetCorrectValues(self, A, B, C, D, E):
        with scenario.Scenario() as s:
            s.some_object( A ) >> B
            s.another_object( C, D ) >> E
            some_object = fake.Fake('some_object')
            another_object = fake.Fake('another_object')
            assert some_object( A ) == B
            assert another_object( C, D ) == E

    def test_TwoFakeCalls_MustBeInOrder( self ):
        class PreventScenarioEndVerifications(Exception): pass
        with pytest.raises(PreventScenarioEndVerifications):
            with scenario.Scenario() as s:
                s.some_object( 10 ).returns( 15 )
                s.another_object( 20, 50 ).returns( 30 )
                some_object = fake.Fake('some_object')
                another_object = fake.Fake('another_object')
                with pytest.raises( testixexception.ExpectationException ):
                    another_object( 20, 50 )

                raise PreventScenarioEndVerifications()

    def test_Four_FakeCalls_MustBeInOrder( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ) >> 15
            s.another_object( 20, 50 ).returns( 30 )
            s.some_object( 'x' ).returns( 'y' )
            s.another_object( 'X', 'Y' ) >> 'Z'
            some_object = fake.Fake('some_object')
            another_object = fake.Fake('another_object')
            assert some_object( 10 ) == 15
            assert another_object( 20, 50 ) == 30
            assert some_object( 'x' ) == 'y'
            assert another_object( 'X', 'Y' ) == 'Z'

    def test_ScenarioEndsPrematurely( self ):
        with pytest.raises( testixexception.ScenarioException ):
            with scenario.Scenario() as s:
                s.some_object( 10 ).returns( 15 )
                s.another_object( 20, 50 ).returns( 30 )
                some_object = fake.Fake('some_object')
                another_object = fake.Fake('another_object')
                assert some_object( 10 ) == 15

    def test_bugfix_ScenarioEndsPrematurely_With_UnorderedCalls( self ):
        with pytest.raises( testixexception.ScenarioException ):
            with scenario.Scenario() as s:
                s.some_object( 10 )
                s.another_object( 20, 50 ).unordered()
                some_object = fake.Fake('some_object')
                another_object = fake.Fake('another_object')
                some_object( 10 )

    def test_CallParametersDontMatch( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).returns( 15 )
            some_object = fake.Fake('some_object')
            with pytest.raises( testixexception.ExpectationException ):
                some_object( 1024 )

    def test_ShiftLeftOperator( self ):
        with scenario.Scenario() as s:
            s <<\
                expectations.Call( 'some_object', 10 ).returns( 15 ) <<\
                expectations.Call( 'some_object', 15 ).returns( 30 )
            some_object = fake.Fake('some_object')
            assert some_object( 10 ) == 15
            assert some_object( 15 ) == 30

    def test_ThrowingCallExpectation( self ):
        class MyException( Exception ): pass

        with scenario.Scenario() as s:
            s.some_object( 10 ).throwing( MyException )
            some_object = fake.Fake('some_object')
            with pytest.raises( MyException ):
                some_object( 10 )

    def test_ThrowingCallExpectation_AlternateSyntax( self ):
        class MyException( Exception ): pass

        with scenario.Scenario() as s:
            s.some_object( 10 ) >> DSL.Throwing( MyException )
            some_object = fake.Fake('some_object')
            with pytest.raises( MyException ):
                some_object( 10 )

    @hypothesis.given( values=strategies.permutations( [ 10, 11, 12 ] ) )
    def test_UnorderedExpectation( self, values ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).unordered()
            s.some_object( 11 ).unordered()
            s.some_object( 12 ).unordered()

            some_object = fake.Fake('some_object')
            some_object( values[ 0 ] )
            some_object( values[ 1 ] )
            some_object( values[ 2 ] )

    def test_UnorderedExpectationsRunOut( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).unordered()
            s.some_object( 11 ).unordered()

            some_object = fake.Fake('some_object')
            some_object( 11 )
            some_object( 10 )
            with pytest.raises( testixexception.ExpectationException ):
                some_object( 11 )

    def test_EverlastingCall( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).unordered().everlasting()
            s.some_object( 11 ).unordered().everlasting()
            some_object = fake.Fake('some_object')
            some_object( 10 )
            some_object( 10 )
            some_object( 10 )
            some_object( 10 )
            some_object( 11 )
            some_object( 11 )

    def test_Everlasting_Unorderd_and_Regular_Calls( self ):
        with scenario.Scenario() as s:
            s.everlasting( 10 ).returns( 'ten' ).unordered().everlasting()
            s.everlasting( 11 ).returns( 'eleven' ).unordered().everlasting()
            s.unordered( 20 ).returns( 'twenty' ).unordered()
            s.unordered( 19 ).returns( 'nineteen' ).unordered()
            s.ordered( 1 ).returns( 'one' )
            s.ordered( 2 ).returns( 'two' )
            s.ordered( 3 ).returns( 'three' )

            ordered = fake.Fake('ordered')
            everlasting = fake.Fake('everlasting')
            unordered = fake.Fake('unordered')

            assert everlasting( 10 ) == 'ten'
            assert ordered( 1 ) == 'one'
            assert ordered( 2 ) == 'two'
            assert everlasting( 10 ) == 'ten'
            assert everlasting( 11 ) == 'eleven'
            assert everlasting( 11 ) == 'eleven'
            assert everlasting( 10 ) == 'ten'
            assert ordered( 3 ) == 'three'
            assert everlasting( 11 ) == 'eleven'
            assert unordered( 20 ) == 'twenty'
            assert everlasting( 10 ) == 'ten'
            assert unordered( 19 ) == 'nineteen'
            assert everlasting( 10 ) == 'ten'

    def test_Everlasting_Calls_Have_ArgumentExpectations( self ):
        with scenario.Scenario() as s:
            s.some_object( 10 ).returns( 'ten' ).unordered().everlasting()

            some_object = fake.Fake('some_object')
            assert some_object( 10 ) == 'ten'
            with pytest.raises( testixexception.ExpectationException ):
                some_object( 11 )

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

            some_object = fake.Fake('some_object')
            some_object( 10 )
            assert len( func1Calls ) == 2
            assert func1Calls[ 0 ] == ( ( 10, 20 ), { 'name': 'Moshe' } )
            assert func1Calls[ 1 ] == ( ( 70, 80 ), { 'name': 'Avraham' } )
            some_object( 11 )
            assert len( func1Calls ) == 3
            func1Calls[ 2 ] == ( 11, 21 ), { 'name': 'Haim' }
    
    def test_fake_context(self):
        tempfile_mock = fake.Fake('tempfile')
        with scenario.Scenario() as s:
            s.tempfile.TemporaryFile() >> fake_context.FakeContext('temp_file')
            s.temp_file.read()

            with tempfile_mock.TemporaryFile() as f:
                f.read()

    def test_fake_context_returns_string(self):
        tempfile_mock = fake.Fake('tempfile')
        read_mock = fake.Fake('read')
        with scenario.Scenario() as s:
            s.tempfile.TemporaryDirectory() >> fake_context.FakeContext('temp_folder').__entry_value__('/path/to/dir')
            s.read('/path/to/dir')

            with tempfile_mock.TemporaryDirectory() as folder:
                read_mock(folder)

    def test_dynamic_fake_names(self):
        with scenario.Scenario() as s:
            s.__dynamic__('some_object')(33) >> 44
            fakeObject = fake.Fake('some_object')
            assert fakeObject(33) == 44

    def test_expectation_from_fake_objects(self):
        with scenario.Scenario() as s:
            fakeObject = fake.Fake('some_object')
            s.__from_fake__(fakeObject)(33) >> 44
            assert fakeObject(33) == 44

    def test_scenario_resets_properties_on_fakes(self):
        with scenario.Scenario() as s:
            fakeObject = fake.Fake('some_object')
            fake.Fake('some_object').name = 'haim'
            fake.Fake('some_object').age = 40
            assert fakeObject.age == 40
            assert fakeObject.name == 'haim'

        with scenario.Scenario() as s:
            fake.Fake('some_object').height = 180
            assert fake.Fake('some_object').height == 180
            assert type(fakeObject.age) is fake.Fake
            assert type(fakeObject.haim) is fake.Fake

        with scenario.Scenario() as s:
            fakeObject = fake.Fake('some_object')
            assert type(fakeObject.height) is fake.Fake
            assert type(fakeObject.age) is fake.Fake
            assert type(fakeObject.haim) is fake.Fake

    @pytest.mark.asyncio
    async def test_async_expectations(self):
        with scenario.Scenario('awaitable test') as s:
            fakeObject = fake.Fake('some_object')
            s.__await_on__().some_object('wtf') >> 555
            assert await fakeObject('wtf') == 555

        with scenario.Scenario('awaitable chain test') as s:
            fakeObject = fake.Fake('some_object')
            s.__await_on__().some_object.some_attribute.another_method('wtf') >> 777
            assert await fakeObject.some_attribute.another_method('wtf') == 777

        with scenario.Scenario('awaitable throws') as s:
            class MyException( Exception ): pass
            s.__await_on__().some_object( 10 ) >> DSL.Throwing( MyException )
            with pytest.raises( MyException ):
                await fakeObject( 10 )
