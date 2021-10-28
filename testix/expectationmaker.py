from testix import expectations

class ExpectationMaker:
    def __init__( self, scenario, scenarioMocks, path, awaitable, is_context ):
        self._scenario = scenario
        self._scenarioMocks = scenarioMocks
        self._path = path
        self._awaitable = awaitable
        self.__is_context = is_context

    def __getattr__( self, name ):
        childPath = f'{self._path}.{name}'
        return ExpectationMaker( self._scenario, self._scenarioMocks, childPath, self._awaitable, self.__is_context )

    def __call__( self, * args, ** kwargs ):
        call = expectations.Call( self._path, * args, ** kwargs )
        call.awaitable(self._awaitable)
        call.context_manager(self.__is_context)
        self._scenario.addEvent( call )
        return call
