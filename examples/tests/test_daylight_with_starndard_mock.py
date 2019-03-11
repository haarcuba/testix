import pytest
from unittest.mock import patch
from unittest.mock import Mock

from examples import daylight
class FakeDay( object ):
    def __add__( self, other ):
            return other

class Test_Daylight:
    def module_patch( self, patch_module ):
        patch_module( daylight, 'datetime' )

    @patch('examples.daylight.datetime')
    def test_Main( self, datetime ):
        fakeDay = FakeDay()
        fakeDay.hour = 12
        datetime.date.today = Mock(side_effect=[fakeDay])
        datetime.datetime.today = Mock(side_effect=[fakeDay])
        datetime.datetime.timedelta = Mock(side_effect=[FakeDay()])
        nextDay = daylight.nextDaylightDate()
        assert nextDay is not fakeDay
        datetime.date.today.assert_called_once_with()
        datetime.datetime.today.assert_called_once_with()
        datetime.timedelta.assert_called_once()

    @patch('examples.daylight.datetime')
    def test_EarlyInTheMorningUsesSameDate( self, datetime ):
        fakeDay = FakeDay()
        fakeDay.hour = 2
        datetime.date.today = Mock(side_effect=[fakeDay])
        datetime.datetime.today = Mock(side_effect=[fakeDay])
        nextDay = daylight.nextDaylightDate()
        assert nextDay is fakeDay
        datetime.date.today.assert_called_once_with()
        datetime.datetime.today.assert_called_once_with()
