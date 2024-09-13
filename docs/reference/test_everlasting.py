from testix import *


def test_unordered_expecation():
    with Scenario() as s:
        s.some_object('a')
        s.some_object('b')
        s.some_object('c').unordered().everlasting()

        my_fake = Fake('some_object')
        my_code(my_fake)


def my_code(x):
    x('c')
    x('c')
    x('c')

    x('a')
    x('c')
    x('b')

    x('c')
    x('c')
