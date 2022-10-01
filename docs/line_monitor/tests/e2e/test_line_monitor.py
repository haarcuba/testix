import line_monitor.monitor
import line_monitor.capture_lines

def test_line_monitor():
    captured_lines = []
    tested = line_monitor.Monitor()
    tested.register_callback(captured_lines.append)
    PRINT_10_LINES_COMMAND = ['python', '-c', 'for i in range(10): print(f"line {i}")']
    tested.launch_subprocess(PRINT_10_LINES_COMMAND)
    tested.wait()
    EXPECTED_LINES = [f'line {i}' for i in range(10)]
    assert captured_lines == EXPECTED_LINES
