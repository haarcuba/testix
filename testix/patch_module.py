import pytest
from testix import fake

_SENTINEL = 'testix-sentinel-a72004be-7a66-42f5-bdcf-7d71eb7283e3'

class Patcher:
    def __init__(self):
        self.__stack = []

    def __call__(self, module, attribute, mock = None):
        if hasattr( module, attribute ):
            original = getattr( module, attribute )
        else:
            original = _SENTINEL
        if mock is None:
            mock = fake.Fake(attribute)
        setattr( module, attribute, mock )
        self.__stack.append( ( module, attribute, original ) )
        return mock

    def undo(self):
        for module, attribute, original in reversed(self.__stack):
            if original is _SENTINEL:
                delattr(module, attribute)
            else:
                setattr(module, attribute, original)

@pytest.fixture
def patch_module():
    patcher = Patcher()
    yield patcher
    patcher.undo()
