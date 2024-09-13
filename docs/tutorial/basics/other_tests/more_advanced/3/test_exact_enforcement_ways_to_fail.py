import pytest
from testix import *


def go1(source, destination):
    names = source.get_names(spec='all', order='lexicographic', ascending=True)
    destination.put_names(names)


def go2(source, destination):
    names = source.get_names('all', True, order='lexicographic')
    destination.put_names(names)


def go3(source, destination):
    names = source.get_names('all', 'lexicographic', True)
    destination.put_names(names)


def go4(source, destination):
    names = source.get_names('all', order='lexicographic', ascending=True)
    destination.put_names(names)
    destination.something_else()


@pytest.fixture(params=[go1, go2, go3, go4])
def go(request):
    return request.param


def test_my_code(go):
    with Scenario() as s:
        s.source.get_names('all', order='lexicographic', ascending=True) >> ['some', 'names']
        s.destination.put_names(['some', 'names'])

        go(Fake('source'), Fake('destination'))
