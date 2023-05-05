import aiofiles

async def go(filename):
    async with aiofiles.open(filename) as f:
        return await f.read()
