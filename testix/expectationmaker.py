from testix import expectations

class ExpectationMaker:
    def __init__( self, scenario, scenarioMocks, path ):
        self._scenario = scenario
        self._scenarioMocks = scenarioMocks
        self._path = path

    def __getattr__( self, name ):
        childPath = f'{self._path}.{name}'
        return ExpectationMaker( self._scenario, self._scenarioMocks, childPath )

    def __call__( self, * args, ** kwargs ):
        call = expectations.Call( self._path, * args, ** kwargs )
        self._scenario.addEvent( call )
        return call
