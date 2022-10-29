from testix import *
import pytest
import line_monitor

@pytest.fixture
def override_imports(patch_module):
    patch_module(line_monitor, 'subprocess')
    patch_module(line_monitor, 'pty')
    patch_module(line_monitor, 'open')

def launch_scenario(s):
    s.pty.openpty() >> ('write_to_fd', 'read_from_fd')
    s.open('read_from_fd', encoding='latin-1') >> Fake('reader')
    s.subprocess.Popen(['my', 'command', 'line'], stdout='write_to_fd', close_fds=True)

def test_lauch_subprocess_with_pseudoterminal(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

def test_receive_output_lines_via_callback(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

        s.reader.readline() >> 'line 1'
        s.my_callback('line 1')
        s.reader.readline() >> 'line 2'
        s.my_callback('line 2')
        s.reader.readline() >> 'line 3'
        s.my_callback('line 3')
        s.reader.readline() >> Throwing(TestixLoopBreaker) # this tells the Fake('reader') to raise an instance of TestixLoopBreaker()

        tested.register_callback(Fake('my_callback'))
        with pytest.raises(TestixLoopBreaker):
            tested.monitor()
