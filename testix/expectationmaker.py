from testix import expectations

class ExpectationMaker:
    def __init__( self, scenario, scenarioMocks, path, awaitable, is_context ):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__awaitable = awaitable
        self.__is_context = is_context

    def __getattr__( self, name ):
        childPath = f'{self.__path}.{name}'
        return ExpectationMaker( self.__scenario, self.__scenarioMocks, childPath, self.__awaitable, self.__is_context )

    def __call__( self, * args, ** kwargs ):
        call = expectations.Call(self.__path, *args, **kwargs)
        call.awaitable(self.__awaitable)
        call.context_manager(self.__is_context)
        self.__scenario.addEvent(call)
        if self.__is_context:
            entry_call = expectations.Call(call.context_wrapper.entry_expectation_path)
            self.__scenario.addEvent(entry_call)
        return call
