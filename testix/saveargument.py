from testix import argumentexpectations

_saved = {}


class SaveArgument(argumentexpectations.ArgumentExpectation):
    def __init__(self, saveTo):
        self.__saveTo = saveTo
        argumentexpectations.ArgumentExpectation.__init__(self, None)

    def ok(self, value):
        _saved[self.__saveTo] = value
        return True

    def __repr__(self):
        return '|SAVE|'


def saved():
    global _saved
    return _saved
