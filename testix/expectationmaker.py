from . import call_character
from testix import testixexception
import testix.expectations.call
from testix import expectations
from testix import trivial
from testix import awaitable
from testix import context_wrapper
import testix.context_wrapper.synchronous
import testix.context_wrapper.asynchronous

class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, character: call_character.CallCharacter):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__character = character

    def __getattr__( self, name ):
        childPath = f'{self.__path}.{name}'
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, childPath, self.__character)

    def __call__(self, *args, **kwargs):
        call = self.__generate_expectation(*args, **kwargs)
        self.__scenario.addEvent(call)
        if call.extra_path is not None:
            extra = expectations.call.Call(call.extra_path, trivial.Trivial)
            self.__scenario.addEvent(extra)
        return call

    def __generate_expectation(self, *args, **kwargs):
        if self.__character.normal:
            modifier = trivial.Trivial
        if self.__character.awaitable:
            modifier = awaitable.Awaitable
        if self.__character.is_sync_context:
            modifier = context_wrapper.synchronous.Synchronous
        if self.__character.is_async_context:
            modifier = context_wrapper.asynchronous.Asynchronous

        return expectations.call.Call(self.__path, modifier, *args, **kwargs)
