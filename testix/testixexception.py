import unittest


class TestixError(Exception):
    pass


class TestixException(unittest.TestCase.failureException):
    pass


class ScenarioException(TestixException):
    pass


class ExpectationException(TestixException):
    pass
