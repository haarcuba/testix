import hypothesis
import hypothesis.strategies as strategies
import pytest
from testix import fake
from testix import testixexception


class TestFakeObject:
    @hypothesis.given(text=strategies.text())
    def test_CallingFakeObject_WhileNoScenario_MustThrow(self, text):
        fakeObject = fake.Fake('hi_there')
        with pytest.raises(testixexception.TestixError):
            fakeObject(text)

    def test_FakeObjectImplicitCreation_OnlyOnce(self):
        fakeObject = fake.Fake('hi_there')
        b1 = fakeObject.b
        b2 = fakeObject.b
        assert b1 is b2

    def test_FakeObjectCreation_OnlyOnce(self):
        fakeObject1 = fake.Fake('hi_there')
        fakeObject2 = fake.Fake('hi_there')
        assert fakeObject1 is fakeObject2
