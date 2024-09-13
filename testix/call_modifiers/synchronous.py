from testix import fake
from testix import fake_privacy_violator
import uuid
from . import base


class Synchronous(base.Base):
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__enter_mock = fake.Fake('{call}@{id}.__enter__'.format(call=call, id=id))

    def __enter__(self):
        self.__enter_mock()
        return self.__result

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def extra_path(self):
        return fake_privacy_violator.path(self.__enter_mock)

    def set_result(self, value):
        self.__result = value

    def throwing(self, exception_factory):
        pass

    def result(self):
        return self

    def __repr__(self):
        return 'Synchronous({})'.format(self.__result)
