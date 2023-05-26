import pytest
from testix import *

import temporary_storage

@pytest.fixture(autouse=True)
def mock_builtin(patch_module):
    patch_module(temporary_storage, 'open')

class StartsWith(ArgumentExpectation):
    def ok(self, value):
        return value.startswith(self.expectedValue)

def test_person_connects_somehow():
    with Scenario() as s:
        s.open(StartsWith('/tmp/'), 'w') >> Fake('the_file')
        s.the_file.write('file_name: some_file\n\n')

        tested = temporary_storage.TemporaryStorage()
        the_file = tested.create_file('some_file')
        assert the_file is Fake('the_file')
