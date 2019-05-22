from . import fakeobject

class FakeContext(fakeobject.FakeObject):
    def __enter__(self):
        return self

    def __exit__(self, * args):
        pass
