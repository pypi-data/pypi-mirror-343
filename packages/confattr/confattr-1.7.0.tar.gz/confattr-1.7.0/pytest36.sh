#!/usr/bin/env bash

# tox is no longer able to test against python 3.6
# run this file instead of tox -e py36

color_warning='[33m'
color_reset='[m'

if ! which python3.6 &>/dev/null; then
	echo "${color_warning}python3.6 is not installed, skipping this test${color_reset}"
	exit
fi

if [ ! -d venv36 ]; then
	python3.6 -m venv venv36
	venv36/bin/pip install --upgrade pip
	venv36/bin/pip install -e .
	venv36/bin/pip install pytest pytest-reporter-html-dots
	venv36/bin/pip install dataclasses  # used in tests
	venv36/bin/pip install urwid  # used in examples
fi

TOX_ENV_NAME=py36 venv36/bin/pytest "$@"
