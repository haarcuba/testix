import hypothesis
import hypothesis.strategies as strategies
import pytest
from testix import fakeobject
from testix import testixexception

class TestArgumentExpectations:
    @hypothesis.given(text=strategies.text())
    def test_CallingFakeObject_WhileNoScenario_MustThrow(self, text):
        fakeObject = fakeobject.FakeObject('hi_there')	
        with pytest.raises( testixexception.TestixException ):
            fakeObject(text)

    def test_FakeObjectImplicitCreation_OnlyOnce( self ):
        fakeObject = fakeobject.FakeObject('hi_there')	
        b1 = fakeObject.b
        b2 = fakeObject.b
        assert b1 is b2

    def test_FakeObjectCreation_OnlyOnce( self ):
        fakeObject1 = fakeobject.FakeObject('hi_there')
        fakeObject2 = fakeobject.FakeObject('hi_there')
        assert fakeObject1 is fakeObject2
