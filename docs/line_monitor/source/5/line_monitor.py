import subprocess
import pty

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
        subprocess.Popen(*popen_args, **popen_kwargs)

    def monitor(self):
        for _ in range(3):
            line = self._reader.readline()
            self._callback(line)
