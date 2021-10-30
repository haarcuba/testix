from . import modifiers
from testix import testixexception
from testix.expectations import normal_call
from testix.expectations import awaitable_call
from testix.expectations import async_context_call
from testix.expectations import sync_context_call

class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, modifiers_: modifiers.Modifiers):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__modifiers = modifiers_

    def __getattr__( self, name ):
        childPath = f'{self.__path}.{name}'
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, childPath, self.__modifiers)

    def __call__(self, *args, **kwargs):
        call, extra_path = self.__generate_expectation(*args, **kwargs)
        self.__scenario.addEvent(call)
        if extra_path is not None:
            extra = normal_call.NormalCall(extra_path)
            self.__scenario.addEvent(extra)
        return call

    def __generate_expectation(self, *args, **kwargs):
        if self.__modifiers.normal:
            return normal_call.NormalCall(self.__path, *args, **kwargs), None
        if self.__modifiers.awaitable:
            call = awaitable_call.AwaitableCall(self.__path, *args, **kwargs)
            return call, call.await_expectation.await_expectation_path
        if self.__modifiers.is_sync_context:
            call = sync_context_call.SyncContextCall(self.__path, *args, **kwargs)
            return call, call.context_wrapper.entry_expectation_path
        if self.__modifiers.is_async_context:
            call = async_context_call.AsyncContextCall(self.__path, *args, **kwargs)
            return call, call.context_wrapper.entry_expectation_path

        raise testixexception.TestixError(f'could not determine expectation type for {args}, {kwargs}')
