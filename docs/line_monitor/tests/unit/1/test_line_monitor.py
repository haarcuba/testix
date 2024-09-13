from testix import *
import pytest
import line_monitor


@pytest.fixture
def override_imports(patch_module):
    patch_module(line_monitor, 'subprocess')  # this replaces the subprocess object inside line_monitor with a Fake("subprocess") object
    patch_module(line_monitor, 'pty')  # does the same for the pty module


def test_lauch_subprocess_with_pseudoterminal(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        s.pty.openpty() >> ('write_to_fd', 'read_from_fd')
        s.subprocess.Popen(['my', 'command', 'line'], stdout='write_to_fd', close_fds=True)

        tested.launch_subprocess(['my', 'command', 'line'])
