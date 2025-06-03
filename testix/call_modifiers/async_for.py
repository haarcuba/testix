from testix import fake
from testix import fake_privacy_violator
import uuid
from . import base


class AsyncFor(base.Base):
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__aiter_mock = fake.Fake('{call}@{id}.__aiter__'.format(call=call, id=id))

    async def __aiter__(self):
        self.__aiter_mock()
        return self.__result

    async def __aexit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def extra_path(self):
        return fake_privacy_violator.path(self.__aiter_mock)

    def set_result(self, value):
        self.__result = value

    def throwing(self, exception_factory):
        pass

    def result(self):
        return self

    def __repr__(self):
        return 'AsyncFor({})'.format(self.__result)
