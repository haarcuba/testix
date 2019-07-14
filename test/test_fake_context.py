from testix import fake
from testix import fake_context
from testix import testixexception


def test_fake_context():
    with fake_context.FakeContext('context') as mock:
        assert mock is fake.Fake('context')

def test_fake_context_as_something():
    with fake_context.FakeContext('context', 'thing') as mock:
        assert mock is 'thing'
