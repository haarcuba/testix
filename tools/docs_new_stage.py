import argparse
import pathlib
import os
import shutil
import box

class Folders:
    def __init__(self, number):
        self.number = number
        root = pathlib.Path('docs/line_monitor/').absolute()
        self.root = root
        self.test = root / f'tests/unit/{number}'
        self.source = root / f'source/{number}'
        self.test.mkdir()
        self.source.mkdir()

        self.previous = box.Box()
        self.previous.test = root / f'tests/unit/{number - 1}'
        self.previous.source = root / f'source/{number - 1}'

def go_test(folders):
    previous = folders.number - 1
    os.chdir(folders.source)
    os.symlink(f'../{previous}/line_monitor.py', 'line_monitor.py')
    os.chdir(folders.test)
    shutil.copy(f'../{previous}/test_line_monitor.py', '.')

def go_source(folders):
    previous = folders.number - 1
    os.chdir(folders.test)
    os.symlink(f'../{previous}/test_line_monitor.py', 'test_line_monitor.py')
    os.chdir(folders.source)
    shutil.copy(f'../{previous}/line_monitor.py', '.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('kind', choices=['test', 'code'])
    arguments = parser.parse_args()

    folders = Folders(arguments.number)
    if arguments.kind == 'test':
        go_test(folders)
    else:
        go_source(folders)


if __name__ == '__main__':
    main()
