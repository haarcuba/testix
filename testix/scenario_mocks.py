from testix import expectationmaker

class ScenarioMocks:
    def __init__( self, scenario ):
        self._scenario = scenario

    def __dynamic__(self, name):
        return getattr(self, name)

    def __getattr__( self, name ):
        return expectationmaker.ExpectationMaker( self._scenario, self, name )

    def __lshift__( self, expectation ):
        self._scenario.addEvent( expectation )
        return self
