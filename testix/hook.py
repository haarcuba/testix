class Hook:
    def __init__(self, callable, *args, **kwargs):
        self.__callable = callable
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        self.__callable(*self.__args, **self.__kwargs)
