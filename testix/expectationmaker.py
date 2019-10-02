from testix import expectations

class ExpectationMaker:
    def __init__( self, scenario, scenarioMocks, path, awaitable ):
        self._scenario = scenario
        self._scenarioMocks = scenarioMocks
        self._path = path
        self._awaitable = awaitable

    def __getattr__( self, name ):
        childPath = f'{self._path}.{name}'
        return ExpectationMaker( self._scenario, self._scenarioMocks, childPath, self._awaitable )

    def __call__( self, * args, ** kwargs ):
        call = expectations.Call( self._path, * args, ** kwargs )
        call.awaitable(self._awaitable)
        self._scenario.addEvent( call )
        return call
