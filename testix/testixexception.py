import unittest

class TestixException( unittest.TestCase.failureException ): pass
class ScenarioException( TestixException ): pass
class ExpectationException( TestixException ): pass
