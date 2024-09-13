from testix import *
import my_code


def test_my_code():
    with Scenario() as s:
        s.source.get_names('all', order='lexicographic', ascending=True) >> ['some', 'names']
        s.destination.put_names(['some', 'names'])

        my_code.go(Fake('source'), Fake('destination'))
