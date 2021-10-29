from . import expectationmaker
from . import fake_privacy_violator
from . import modifiers

class ScenarioMocks:
    def __init__( self, scenario ):
        self.__awaitable = False
        self.__scenario = scenario
        self.__modifiers = modifiers.Modifiers()

    def __dynamic__(self, name):
        return getattr(self, name)

    def __from_fake__(self, fake):
        path = fake_privacy_violator.path(fake)
        return getattr(self, path)

    def __getattr__( self, name ):
        modifiers_ = modifiers.Modifiers(self.__modifiers)
        self.__reset_modifiers()
        return expectationmaker.ExpectationMaker(self.__scenario, self, name, modifiers_)

    def __reset_modifiers(self):
        self.__modifiers = modifiers.Modifiers()

    def __lshift__( self, expectation ):
        self.__scenario.addEvent(expectation)
        return self

    @property
    def __with__(self):
        self.__modifiers.is_context = True
        return self

    @property
    def __await_on__(self):
        self.__modifiers.awaitable = True
        return self
