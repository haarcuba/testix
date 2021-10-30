import uuid
from testix import fake
from testix import fake_privacy_violator

class Awaitable:
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__await_mock = fake.Fake(f'await on {call}@{id}')
        self.__exception = None

    async def __call__(self):
        self.__await_mock()
        if self.__exception is not None:
            raise self.__exception
        return self.__result

    def set_result(self, result):
        self.__result = result

    def throwing(self, exception):
        self.__exception = exception

    @property
    def await_expectation_path(self):
        return fake_privacy_violator.path(self.__await_mock)
