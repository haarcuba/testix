import subprocess
import pty
import select


class LineMonitor:
    def __init__(self):
        self._callback = None

    def register_callback(self, callback):
        self._callback = callback

    def launch_subprocess(self, *popen_args, **popen_kwargs):
        write_to, read_from = pty.openpty()
        popen_kwargs['stdout'] = write_to
        popen_kwargs['close_fds'] = True
        self._reader = open(read_from, encoding='latin-1')
        self._poller = select.poll()
        self._poller.register(self._reader.fileno(), select.POLLIN)
        subprocess.Popen(*popen_args, **popen_kwargs)

    def monitor(self):
        while True:
            if not self._data_available_to_read():
                continue
            line = self._reader.readline()
            if self._callback is None:
                continue
            self._callback(line)

    def _data_available_to_read(self):
        poll_results = self._poller.poll()
        _, events = poll_results[0]
        return events & select.POLLIN
