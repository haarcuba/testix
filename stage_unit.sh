#!/bin/bash
STAGE=$1
PYTHONPATH=docs/line_monitor/source/$STAGE  python -m pytest -sv docs/line_monitor/tests/unit/$STAGE/

