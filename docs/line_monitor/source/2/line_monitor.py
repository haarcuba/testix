import subprocess
import pty

class LineMonitor:
    def register_callback(self, callback):
        pass

    def launch_subprocess(self, *popen_args, **popen_kwargs):
        write_to, read_from = pty.openpty()
        popen_kwargs['stdout'] = write_to
        popen_kwargs['close_fds'] = True
        subprocess.Popen(*popen_args, **popen_kwargs)

    def wait(self):
        pass
