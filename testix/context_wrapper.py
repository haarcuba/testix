class ContextWrapper:
    def __init__(self, result):
        self.__result = result

    def __enter__(self):
        return self.__result

    def __exit__(self, exception_type, exception_value, traceback):
        pass
