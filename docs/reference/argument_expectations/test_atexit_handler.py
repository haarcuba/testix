from testix import *
import pytest
import robot


@pytest.fixture
def mock_imports(patch_module):
    patch_module(robot, 'atexit')  # mock atexit module


def test_atexit_handler(mock_imports):
    with Scenario() as s:
        s.atexit.register(saveargument.SaveArgument('the_handler'))

        tested = robot.Robot(cleanup_func=Fake('cleanup_logic'))

        handler = saveargument.saved()['the_handler']
        s.cleanup_logic(1, 2, 3)

        handler()
