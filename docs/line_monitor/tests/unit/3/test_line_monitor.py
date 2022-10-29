from testix import *
import pytest
import line_monitor

@pytest.fixture
def override_imports(patch_module):
    patch_module(line_monitor, 'subprocess') # this replaces the subprocess object inside line_monitor with a Fake("subprocess") object
    patch_module(line_monitor, 'pty') # does the same for the pty module
    patch_module(line_monitor, 'open')

def test_lauch_subprocess_with_pseudoterminal(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        s.pty.openpty() >> ('write_to_fd', 'read_from_fd')
        s.subprocess.Popen(['my', 'command', 'line'], stdout='write_to_fd', close_fds=True)

        tested.launch_subprocess(['my', 'command', 'line'])

def test_receive_output_lines_via_callback(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        s.pty.openpty() >> ('write_to_fd', 'read_from_fd')
        s.open('read_from_fd', encoding='latin-1') >> Fake('reader') # wrapping a binary file descriptor with a text-oriented stream requires an encoding
        s.subprocess.Popen(['my', 'command', 'line'], stdout='write_to_fd', close_fds=True)

        tested.launch_subprocess(['my', 'command', 'line'])

        s.reader.readline() >> 'line 1'
        s.my_callback('line 1')
        s.reader.readline() >> 'line 2'
        s.my_callback('line 2')
        s.reader.readline() >> 'line 3'
        s.my_callback('line 3')

        tested.register_callback(Fake('my_callback'))
        tested.monitor()
