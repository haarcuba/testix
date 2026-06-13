from . import base


class Trivial(base.Base):
    def __init__(self, call):
        self.__result = None
        self.__exception_factory = None

    def set_result(self, value):
        self.__result = value

    def result(self):
        if self.__exception_factory:
            raise self.__exception_factory()
        return self.__result

    def throwing(self, exception_factory):
        self.__exception_factory = exception_factory

    @property
    def extra_path(self):
        return None
