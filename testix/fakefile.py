from testix import fakeobject


class FakeFile( fakeobject.FakeObject ):
    def __enter__( self ):
        return self

    def __exit__( self, * args ):
        self.close()
