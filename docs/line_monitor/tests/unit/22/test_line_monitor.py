from testix import *
import pytest
import line_monitor
import select


@pytest.fixture
def override_imports(patch_module):
    patch_module(line_monitor, 'subprocess')
    patch_module(line_monitor, 'pty')
    patch_module(line_monitor, 'open')
    patch_module(line_monitor, 'select')
    Fake('select').POLLIN = select.POLLIN


def launch_scenario(s):
    s.pty.openpty() >> ('write_to_fd', 'read_from_fd')
    s.open('read_from_fd', encoding='latin-1') >> Fake('reader')
    s.select.poll() >> Fake('poller')
    s.reader.fileno() >> 'reader_descriptor'
    s.poller.register('reader_descriptor', select.POLLIN)
    s.subprocess.Popen(['my', 'command', 'line'], stdout='write_to_fd', close_fds=True) >> Fake('the_process')


def test_lauch_subprocess_with_pseudoterminal(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])


def read_line_scenario(s, line):
    s.poller.poll(IgnoreArgument()) >> [('reader_descriptor', select.POLLIN)]
    s.reader.readline() >> line


def skip_line_scenario(s):
    s.poller.poll(IgnoreArgument()) >> [('reader_descriptor', 0)]


def skip_line_on_empty_poll_scenario(s):
    s.poller.poll(IgnoreArgument()) >> []


def process_lives_scenario(s):
    s.the_process.poll() >> None


def end_test_scenario(s):
    s.poller.poll(IgnoreArgument()) >> Throwing(loop_breaker.LoopBreaker)


def test_receive_output_lines_via_callback(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

        read_line_scenario(s, 'line 1')
        s.my_callback('line 1')
        read_line_scenario(s, 'line 2')
        s.my_callback('line 2')
        read_line_scenario(s, 'line 3')
        s.my_callback('line 3')
        skip_line_scenario(s)
        process_lives_scenario(s)
        skip_line_scenario(s)
        process_lives_scenario(s)
        skip_line_on_empty_poll_scenario(s)
        process_lives_scenario(s)
        read_line_scenario(s, 'line 4')
        s.my_callback('line 4')
        end_test_scenario(s)

        tested.register_callback(Fake('my_callback'))
        with pytest.raises(loop_breaker.LoopBreaker):
            tested.monitor()


def test_monitoring_with_no_callback(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

        read_line_scenario(s, 'line 1')
        read_line_scenario(s, 'line 2')
        skip_line_scenario(s)
        process_lives_scenario(s)
        read_line_scenario(s, 'line 3')
        skip_line_scenario(s)
        process_lives_scenario(s)
        read_line_scenario(s, 'line 4')
        skip_line_on_empty_poll_scenario(s)
        process_lives_scenario(s)
        end_test_scenario(s)

        with pytest.raises(loop_breaker.LoopBreaker):
            tested.monitor()


def test_callback_registered_mid_monitoring(override_imports):
    tested = line_monitor.LineMonitor()
    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

        read_line_scenario(s, 'line 1')
        skip_line_scenario(s)
        process_lives_scenario(s)
        read_line_scenario(s, 'line 2')
        skip_line_on_empty_poll_scenario(s)
        process_lives_scenario(s)
        read_line_scenario(s, 'line 3')
        s << Hook(tested.register_callback, Fake('my_callback'))  # the hook will execute right after the 'line 3' readline finishes
        s.my_callback('line 3')  # callback is now registered, so it should be called
        end_test_scenario(s)

        with pytest.raises(loop_breaker.LoopBreaker):
            tested.monitor()
