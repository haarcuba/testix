from testix import argumentexpectations
from testix import testixexception
from testix import scenario
from testix import call_formatter
from testix import DSL


class Call:
    def __init__(self, fakeObjectPath, modifier, *arguments, **kwargExpectations):
        self.__fakeObjectPath = fakeObjectPath
        self.__argumentExpectations = [self.__expectation(arg) for arg in arguments]
        self.__kwargExpectations = {name: self.__expectation(kwargExpectations[name]) for name in kwargExpectations}
        self.__unordered = False
        self.__everlasting = False
        self.__modifier = modifier(self)

    @property
    def extra_path(self):
        return self.__modifier.extra_path

    def returns(self, result):
        self.__modifier.set_result(result)
        return self

    def __rshift__(self, result):
        if type(result) is DSL.Throwing:
            self.throwing(result.exceptionFactory)
        else:
            self.returns(result)

    def throwing(self, exceptionFactory):
        self.__modifier.throwing(exceptionFactory)
        return self

    def unordered(self):
        scenario.current().unordered(self)
        self.__unordered = True
        return self

    def everlasting(self):
        self.__everlasting = True
        if not self.__unordered:
            raise testixexception.TestixError("call cannot be everlasting and not unordered")
        return self

    def __expectation(self, arg):
        if isinstance(arg, argumentexpectations.ArgumentExpectation):
            return arg
        defaultExpectation = argumentexpectations.ArgumentEquals
        return defaultExpectation(arg)

    def result(self):
        return self.__modifier.result()

    def __repr__(self):
        return call_formatter.format(self.__fakeObjectPath, self.__argumentExpectations, self.__kwargExpectations)

    def fits(self, fakeObjectPath, args, kwargs):
        if fakeObjectPath != self.__fakeObjectPath:
            return False
        if self.__ignoreCallDetails():
            return True
        if not self.__verifyArguments(args):
            return False
        if not self.__verifyKeywordArguments(kwargs):
            return False
        return True

    def __ignoreCallDetails(self):
        argumentExpectations = list(self.__argumentExpectations)
        if len(argumentExpectations) == 0:
            return False
        first = argumentExpectations[0]
        return type(first) is argumentexpectations.IgnoreCallDetails

    def __verifyArguments(self, args):
        args = list(args)
        argumentExpectations = list(self.__argumentExpectations)
        if len(argumentExpectations) != len(args):
            return False
        while len(argumentExpectations) > 0:
            argumentExpectation = argumentExpectations.pop(0)
            actualArgument = args.pop(0)
            if not argumentExpectation.ok(actualArgument):
                return False
        return True

    def __verifyKeywordArguments(self, kwargs):
        for name, argumentExpectation in self.__kwargExpectations.items():
            if name not in kwargs:
                return False
            actualArgument = kwargs[name]
            if not argumentExpectation.ok(actualArgument):
                return False
        if self.__unexpectedKeyworkArgument(kwargs):
            return False
        return True

    def __unexpectedKeyworkArgument(self, kwargs):
        for name in kwargs:
            if name not in self.__kwargExpectations:
                return True

    def everlasting_(self):
        return self.__everlasting
