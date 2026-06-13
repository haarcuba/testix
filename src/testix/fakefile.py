from testix import fake


class FakeFile(fake.Fake):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
