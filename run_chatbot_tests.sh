#!/bin/bash

export PYTHONPATH=chatbot/src
python -m pytest chatbot/test/test_chatbot.py
