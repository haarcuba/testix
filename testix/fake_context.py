from . import fake

class FakeContext(fake.Fake):
    def __init__(self, path, thing=fake.Fake.SENTINEL):
        fake.Fake.__init__(self, path)
        if thing is fake.Fake.SENTINEL:
            self._thing = self
        else:
            self._thing = thing

    def __enter__(self):
        return self._thing

    def __exit__(self, * args):
        pass
