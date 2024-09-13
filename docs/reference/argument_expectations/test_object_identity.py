import pytest
from testix import *

import classroom


def test_this_will_pass():
    joe = classroom.Person('Joe')
    with Scenario() as s:
        s.mylist.append(ArgumentIs(joe))

        tested = classroom.Classroom(Fake('mylist'))
        tested.enter_original(joe)


def test_this_will_fail():
    joe = classroom.Person('Joe')
    with Scenario() as s:
        s.mylist.append(ArgumentIs(joe))

        tested = classroom.Classroom(Fake('mylist'))
        tested.enter_copy(joe)
