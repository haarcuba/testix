#!/bin/bash
STAGE=$1
echo PYTHONPATH=docs/line_monitor/source/$STAGE python -m pytest --cov=docs/line_monitor/source --cov-report=term-missing -sv docs/line_monitor/tests/unit/$STAGE/
#PYTHONPATH=docs/line_monitor/source/$STAGE  python -m pytest -sv docs/line_monitor/tests/unit/$STAGE/
