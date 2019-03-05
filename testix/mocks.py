class Mocks:
    def __init__( self, scenario ):
        self._scenario = scenario

    def __lshift__( self, expectation ):
        self._scenario.addEvent( expectation )
        return self
