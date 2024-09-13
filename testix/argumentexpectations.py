from testix import fake
import pprint


class ArgumentExpectation:
    def __init__(self, value):
        self.expectedValue = value

    def ok(self, value):
        raise Exception("must override this")

    def __repr__(self):
        WORKAROUND_PFORMAT_BREAKS_LONG_STRINGS = 100000
        return pprint.pformat(self.expectedValue, width=WORKAROUND_PFORMAT_BREAKS_LONG_STRINGS)


class ArgumentEquals(ArgumentExpectation):
    def ok(self, value):
        return self.expectedValue == value


class ArgumentIsFakeObjectWithPath(ArgumentExpectation):
    def ok(self, value):
        if not isinstance(value, fake.Fake):
            return False
        expectedPath = self.expectedValue
        return value is fake.Fake(expectedPath)

    def __repr__(self):
        return "|%s|" % self.expectedValue


class IgnoreArgument(ArgumentExpectation):
    def __init__(self):
        ArgumentExpectation.__init__(self, 0)

    def ok(self, value):
        return True

    def __repr__(self):
        return '|IGNORED|'


class IgnoreCallDetails(ArgumentExpectation):
    def __init__(self):
        ArgumentExpectation.__init__(self, 0)

    def ok(self, value):
        return True

    def __repr__(self):
        return '|ALL_DETAILS_IGNORED|'


class ArgumentIs(ArgumentExpectation):
    def ok(self, value):
        return value is self.expectedValue

    def __repr__(self):
        return '|IS %s|' % self.expectedValue
