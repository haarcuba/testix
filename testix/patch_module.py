import pytest
from testix import fakeobject

_SENTINEL = 'testix-sentinel-a72004be-7a66-42f5-bdcf-7d71eb7283e3'

class Patcher:
    def __init__( self ):
        self._stack = []

    def __call__( self, module, attribute, mock = None ):
        if hasattr( module, attribute ):
            original = getattr( module, attribute )
        else:
            original = _SENTINEL
        if mock is None:
            mock = fakeobject.FakeObject( attribute )
        setattr( module, attribute, mock )
        self._stack.append( ( module, attribute, original ) )
        return mock

    def undo(self):
        for module, attribute, original in reversed( self._stack ):
            if original is _SENTINEL:
                continue
            setattr( module, attribute, original )

@pytest.fixture
def patch_module():
    patcher = Patcher()
    yield patcher
    patcher.undo()
