import unittest

class TestixException( unittest.TestCase.failureException ): pass
class ExpectationException( TestixException ): pass
