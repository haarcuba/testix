from . import fake

class FakeContext(fake.Fake):
    def __enter__(self):
        return self

    def __exit__(self, * args):
        pass
