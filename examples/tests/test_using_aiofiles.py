from testix import *
import pytest

from examples import async_read

@pytest.fixture(autouse=True)
def override_import(patch_module):
    patch_module(async_read, 'aiofiles')

@pytest.mark.asyncio
async def test_read_write_from_async_file():
    with scenario.Scenario() as s:
        s.__async_with__.aiofiles.open('file_name.txt') >> Fake('the_file')
        s.__await_on__.the_file.read() >> 'the text'

        assert 'the text' == await async_read.go('file_name.txt')
