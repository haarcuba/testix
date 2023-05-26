class Robot:
    def __init__(self, cleanup_func):
        self.cleanup_func = cleanup_func
        atexit.register(self._cleanup)

    def _cleanup(self):
        self.cleanup_func(1, 2, 3)
