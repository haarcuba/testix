import pytest
from testix import fake

_SENTINEL = 'testix-sentinel-a72004be-7a66-42f5-bdcf-7d71eb7283e3'


class Patcher:
    def __init__(self):
        self.__stack = []

    def __call__(self, module, attribute, mock=None):
        original = self.__save_original_value(module, attribute)
        if mock is None:
            mock = fake.Fake(attribute)
            fake.Fake.exempt_from_attribute_sweep(mock.path_a62df12dd67848be82c505d63b928725)
        setattr(module, attribute, mock)
        self.__stack.append((module, attribute, original, mock))
        return mock

    def __save_original_value(self, module, attribute):
        if hasattr(module, attribute):
            return getattr(module, attribute)

        return _SENTINEL

    def undo(self):
        for module, attribute, original, mock in reversed(self.__stack):
            if isinstance(mock, fake.Fake):
                fake.Fake.clear_attributes(mock)
                fake.Fake.unexempt_from_attribute_sweep(mock.path_a62df12dd67848be82c505d63b928725)
            if original is _SENTINEL:
                delattr(module, attribute)
            else:
                setattr(module, attribute, original)


@pytest.fixture
def patch_module():
    patcher = Patcher()
    yield patcher
    patcher.undo()
