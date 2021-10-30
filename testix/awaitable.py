class Awaitable:
    def __init__(self, result):
        self.__result = result

    async def __call__(self):
        return self.__result
