import argparse
import shutil
import logging
import pathlib
import os

def test_folder(stage):
    return pathlib.Path(f'docs/line_monitor/tests/unit/{stage}')

def source_folder(stage):
    return pathlib.Path(f'docs/line_monitor/source/{stage}')

def copy(source, destination):
    logging.info(f'cp {source} {destination}')
    shutil.copy(source, destination)

def link(source, destination):
    logging.info(f'ln -s {source} {destination}')
    os.symlink(source, destination)

parser = argparse.ArgumentParser()
parser.add_argument('stage', type=int)
parser.add_argument('source_mode', choices=['link', 'copy'])
parser.add_argument('test_mode', choices=['link', 'copy'])
arguments = parser.parse_args()
logging.basicConfig(level=logging.INFO)


stage = arguments.stage
previous = stage - 1

test_folder(stage).mkdir(parents=True, exist_ok=True)
logging.info(f'created {test_folder(stage)}')
source_folder(stage).mkdir(parents=True, exist_ok=True)
logging.info(f'created {source_folder(stage)}')

if arguments.source_mode == 'copy':
    copy(source_folder(previous) / 'line_monitor.py', source_folder(stage) / 'line_monitor.py')
else:
    link(f'../{previous}/line_monitor.py', source_folder(stage) / 'line_monitor.py')

if arguments.test_mode == 'copy':
    copy(test_folder(previous) / 'test_line_monitor.py', test_folder(stage) / 'test_line_monitor.py')
else:
    link(f'../{previous}/test_line_monitor.py', test_folder(stage) / 'test_line_monitor.py')
