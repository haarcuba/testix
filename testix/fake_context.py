from . import fake

class FakeContext(fake.Fake):
    def __init__(self, path_a62df12dd67848be82c505d63b928725, **attributes):
        fake.Fake.__init__(self, path_a62df12dd67848be82c505d63b928725, **attributes)
        self._thing = self

    def __entry_value__(self, value):
        self._thing = value
        return self

    def __enter__(self):
        return self._thing

    def __exit__(self, * args):
        pass
