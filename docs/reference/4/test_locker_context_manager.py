from testix import *

def test_fake_context():
    locker_mock = Fake('locker')
    with Scenario() as s:
        s.__with__.locker.Lock() >> Fake('locked')
        s.locked.read() >> 'value'
        s.locked.updater.go('another_value')
        my_code(locker_mock)


def my_code(locker):
    with locker.Lock() as locked:
        whatever = locked.read()
        locked.updater.go(f'another_{whatever}')
