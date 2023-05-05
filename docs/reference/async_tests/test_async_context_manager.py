from testix import *
import pytest

@pytest.mark.asyncio
async def test_async_context_managers():
    with scenario.Scenario() as s:
        s.__async_with__.open('/path/to/file', 'rw') >> fake.Fake('my_file')
        s.__await_on__.my_file.read(500) >> 'some text'
        s.my_file.seek(0)
        s.__await_on__.my_file.write('more text') >> 10

        open_mock = fake.Fake('open')
        async with open_mock('/path/to/file', 'rw') as my_file:
            assert await my_file.read(500) == 'some text'
            my_file.seek(0)
            assert await my_file.write('more text') == 10
