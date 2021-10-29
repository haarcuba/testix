from testix import fake
from testix import fake_privacy_violator
import uuid

class Synchronous:
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__enter_mock = fake.Fake(f'{call}@{id}.__enter__')

    def __enter__(self):
        self.__enter_mock()
        return self.__result

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def entry_expectation_path(self):
        return fake_privacy_violator.path(self.__enter_mock)

    def set_entry_value(self, value):
        self.__result = value

    def __repr__(self):
        return f'Synchronous({self.__result})'
