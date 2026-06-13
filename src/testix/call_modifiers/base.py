import abc


class Base(abc.ABC):
    @abc.abstractmethod
    def __init__(self, call):
        pass

    @abc.abstractmethod
    def set_result(self, value):
        pass

    @abc.abstractmethod
    def result(self):
        pass

    @abc.abstractmethod
    def throwing(self, exception_factory):
        pass

    @property
    @abc.abstractmethod
    def extra_path(self):
        pass
