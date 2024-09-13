from testix import *
import pytest


@pytest.mark.asyncio
async def test_async_expectations():
    with scenario.Scenario('awaitable test') as s:
        s.__await_on__.my_fake('some data') >> fake.Fake('another_fake')
        s.__await_on__.another_fake() >> fake.Fake('yet_another')
        s.__await_on__.yet_another() >> Fake('last_one')
        s.last_one.sync_func(1, 2, 3) >> 'sync value'

        assert await my_code(Fake('my_fake')) == 'sync value'


async def my_code(thing):
    another = await thing('some data')
    yet_another = await another()
    last_one = await yet_another()
    return last_one.sync_func(1, 2, 3)
