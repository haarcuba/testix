import pytest
import re
import hypothesis
import hypothesis.strategies as strategies
from testix import scenario
from testix import testixexception
from testix import hook
from testix import fake
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
            s.some_object(A).returns(B)
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
            s.some_object(10).returns(15)
            s.some_object(15).returns(30)
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
        locker_mock = fake.Fake('locker')
        with scenario.Scenario() as s:
            s.__with__.locker.Lock() >> fake.Fake('locked')
            s.locked.read() >> 'value'
            s.locked.updater.go('another_value')

            with locker_mock.Lock() as locked:
                assert locked.read() == 'value'
                locked.updater.go('another_value')

    def test_anonymous_fake_context(self):
        locker_mock = fake.Fake('locker')
        with scenario.Scenario() as s:
            s.__with__.locker.Lock()

            with locker_mock.Lock():
                pass

    def test_enforce_use_of_with_statement_with_context_manager_expectation(self):
        locker_mock = fake.Fake('locker')
        with pytest.raises(testixexception.ScenarioException, match='locker.Lock.*__enter__'):
            with scenario.Scenario() as s:
                s.__with__.locker.Lock()

                locker_mock.Lock()

    def test_fake_context_returns_arbitrary_value(self):
        tempfile_mock = fake.Fake('tempfile')
        read_mock = fake.Fake('read')
        with scenario.Scenario() as s:
            s.__with__.tempfile.TemporaryDirectory() >> '/path/to/dir'
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

    def test_fix_issue_27__path_attribute_is_possible(self):
        with scenario.Scenario() as s:
            fakeObject = fake.Fake('some_object', path='/path/to/nowhere')
            s.some_object.what() >> 'where'

            assert fakeObject.what() == 'where'
            assert fakeObject.path == '/path/to/nowhere'

    def test_scenario_resets_attributes_on_fakes(self):
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
            s.__await_on__.some_object('wtf') >> fake.Fake('another')
            s.another() >> 555
            s.__await_on__.another() >> fake.Fake('yet_another')
            s.__await_on__.yet_another() >> 777

            another = await fakeObject('wtf')
            assert another() == 555
            yet_another = await another()
            assert await yet_another() == 777

        with scenario.Scenario('awaitable chain test') as s:
            fakeObject = fake.Fake('some_object')
            s.__await_on__.some_object.some_attribute.another_method('wtf') >> 777
            assert await fakeObject.some_attribute.another_method('wtf') == 777

        with scenario.Scenario('awaitable throws') as s:
            class MyException( Exception ): pass
            s.__await_on__.some_object( 10 ) >> DSL.Throwing( MyException )
            with pytest.raises( MyException ):
                await fakeObject( 10 )

    @pytest.mark.asyncio
    async def test_async_context_managers(self):
        with scenario.Scenario() as s:
            s.__async_with__.open('/path/to/file', 'rw') >> fake.Fake('my_file')
            s.__await_on__.my_file.read(500) >> 'some text'
            s.my_file.seek(0)
            s.__await_on__.my_file.write('more text') >> 10

            open_mock = fake.Fake('open')
            async with open_mock('/path/to/file', 'rw') as my_file:
                assert await my_file.read(500) == 'some text'
                my_file.seek(0)
                assert await my_file.write('more text') == 10

    @pytest.mark.asyncio
    async def test_async_anonymous_context_managers(self):
        my_file = fake.Fake('my_file')
        with scenario.Scenario() as s:
            s.__async_with__.locker.lock()
            s.__await_on__.my_file.read(500) >> 'some text'

            locker_mock = fake.Fake('locker')

            async with locker_mock.lock():
                assert await my_file.read(500) == 'some text'

    def test_enforce_use_of_with_statement_with_async_context_manager_expectation(self):
        locker_mock = fake.Fake('locker')
        with pytest.raises(testixexception.ScenarioException, match='locker.Lock.*__aenter__'):
            with scenario.Scenario() as s:
                s.__async_with__.locker.Lock()

                locker_mock.Lock()

    def test_setitem_support(self):
        with scenario.Scenario('unexpected call') as s:
            fake_dict = fake.Fake('fake_dict')
            with pytest.raises(testixexception.ExpectationException, match=re.compile('__setitem__.*the_key.*the_value')):
                fake_dict['the_key'] = 'the_value'

        with scenario.Scenario('expectation fulfilled') as s:
            fake_dict = fake.Fake('fake_dict')
            s.fake_dict.__setitem__('the_key', 'the_value')
            fake_dict['the_key'] = 'the_value'

    @pytest.mark.asyncio
    async def test_enforce_awaiting_on_async_expectations(self):
        my_file = fake.Fake('my_file')
        with pytest.raises(testixexception.TestixException):
            with scenario.Scenario() as s:
                s.__await_on__.my_file.write('some text')

                my_file.write('some text')
