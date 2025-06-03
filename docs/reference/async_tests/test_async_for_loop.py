from testix import *
import pytest


@pytest.mark.asyncio
async def test_async_iterator():
    with scenario.Scenario() as s:
        s.__async_for__.my_iterator >> ['a', 'b', 'c']

        async_capitalizer = AsyncCapitalizer(Fake('my_iterator'))
        result = []
        async for item in async_capitalizer:
            result.append(item)
        assert result == ['A', 'B', 'C']


class AsyncCapitalizer:
    def __init__(self, iterable):
        self._iterable = iterable

    async def __aiter__(self):
        async for item in self._iterable:
            yield item.upper()
