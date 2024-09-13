import line_monitor


def test_line_monitor():
    captured_lines = []
    tested = line_monitor.LineMonitor()
    tested.register_callback(captured_lines.append)
    PRINT_10_LINES_COMMAND = ['python', '-c', 'for i in range(10): print(f"line {i}")']
    tested.launch_subprocess(PRINT_10_LINES_COMMAND)
    tested.monitor()
    EXPECTED_LINES = [f'line {i}\n' for i in range(10)]
    assert captured_lines == EXPECTED_LINES
