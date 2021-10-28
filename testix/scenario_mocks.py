from . import expectationmaker
from . import fake_privacy_violator

class ScenarioMocks:
    def __init__( self, scenario ):
        self.__awaitable = False
        self.__scenario = scenario
        self.__is_context = False

    def __dynamic__(self, name):
        return getattr(self, name)

    def __from_fake__(self, fake):
        path = fake_privacy_violator.path(fake)
        return getattr(self, path)

    def __getattr__( self, name ):
        return expectationmaker.ExpectationMaker(self.__scenario, self, name, self.__awaitable, self.__is_context)

    def __lshift__( self, expectation ):
        self.__scenario.addEvent(expectation)
        return self

    @property
    def __with__(self):
        self.__is_context = True
        return self

    @property
    def __await_on__(self):
        self.__awaitable = True
        return self
