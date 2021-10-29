from testix import fake
from testix import fake_privacy_violator
import uuid

class Asynchronous:
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__aenter_mock = fake.Fake(f'{call}@{id}.__aenter__')

    async def __aenter__(self):
        self.__aenter_mock()
        return self.__result

    async def __aexit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def entry_expectation_path(self):
        return fake_privacy_violator.path(self.__aenter_mock)

    def set_entry_value(self, value):
        self.__result = value

    def __repr__(self):
        return f'Asynchronous({self.__result})'
