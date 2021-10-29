from testix import expectations
from . import modifiers

class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, modifiers_: modifiers.Modifiers):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__modifiers = modifiers_

    def __getattr__( self, name ):
        childPath = f'{self.__path}.{name}'
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, childPath, self.__modifiers)

    def __call__( self, * args, ** kwargs ):
        call = expectations.Call(self.__path, *args, **kwargs)
        call.modify(self.__modifiers)
        self.__scenario.addEvent(call)
        if self.__modifiers.is_context or self.__modifiers.is_async_context:
            entry_call = expectations.Call(call.context_wrapper.entry_expectation_path)
            self.__scenario.addEvent(entry_call)
        return call
