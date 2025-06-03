from . import call_character
import testix.expectations.call
import testix.testixexception
from testix import expectations
import testix.call_modifiers.synchronous
import testix.call_modifiers.asynchronous
import testix.call_modifiers.awaitable
import testix.call_modifiers.trivial


class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, character: call_character.CallCharacter):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__character = character

    def __getattr__(self, name):
        return self.__next_expectation_maker(name)

    def __next_expectation_maker(self, name):
        childPath = '{path}.{name}'.format(path=self.__path, name=name)
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, childPath, self.__character)

    def __call__(self, *args, **kwargs):
        call = self.__generate_expectation(*args, **kwargs)
        self.__scenario.addEvent(call)
        if call.extra_path is not None:
            extra = expectations.call.Call(call.extra_path, testix.call_modifiers.trivial.Trivial)
            self.__scenario.addEvent(extra)
        return call

    def __setitem__(self, key, value):
        expectation_maker = self.__next_expectation_maker('__setitem__')
        return expectation_maker(key, value)

    def __generate_expectation(self, *args, **kwargs):
        if self.__character.normal:
            modifier = testix.call_modifiers.trivial.Trivial
        if self.__character.awaitable:
            modifier = testix.call_modifiers.awaitable.Awaitable
        if self.__character.is_sync_context:
            modifier = testix.call_modifiers.synchronous.Synchronous
        if self.__character.is_async_context:
            modifier = testix.call_modifiers.asynchronous.Asynchronous
        if self.__character.is_async_for:
            raise testix.testixexception.TestixError(
                f'Unsupported: async for expectations are supported but not with a function call, see documentation on how to use them properly'
            )

        return expectations.call.Call(self.__path, modifier, *args, **kwargs)

    def __rshift__(self, iterable):
        if not self.__character.is_async_for:
            raise testix.testixexception.TestixError(
                'Unsupported: direct use of >> on fake is only supported in conjuction with __async_for__ modifier'
            )
        async_iterator_path = f'{self.__path}.async_iterator_a62df12dd67848be82c505d63b928725'
        call = expectations.call.Call(async_iterator_path, testix.call_modifiers.trivial.Trivial)
        call >> iterable
        self.__scenario.addEvent(call)
