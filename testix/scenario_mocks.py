from . import expectationmaker
from . import fake_privacy_violator

class ScenarioMocks:
    def __init__( self, scenario ):
        self._scenario = scenario

    def __dynamic__(self, name):
        return getattr(self, name)

    def __from_fake__(self, fake):
        path = fake_privacy_violator.path(fake)
        return getattr(self, path)

    def __getattr__( self, name ):
        return expectationmaker.ExpectationMaker( self._scenario, self, name )

    def __lshift__( self, expectation ):
        self._scenario.addEvent( expectation )
        return self
