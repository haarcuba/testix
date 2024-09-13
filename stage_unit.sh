#!/bin/bash
set -x
STAGE=$1
export PYTHONPATH=docs/line_monitor/source/$STAGE
python -m pytest --cov=docs/line_monitor/source --cov-report=term-missing -sv docs/line_monitor/tests/unit/$STAGE/
