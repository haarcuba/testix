from testix import fakeobject
from testix import fake_context
from testix import testixexception


def test_fake_context():
    with fake_context.FakeContext('context') as fake:
        assert fake is fakeobject.FakeObject('context')
