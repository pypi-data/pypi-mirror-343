#!../../../../venv/bin/python3

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from type_regex.example_usage import App
a = App()
if True:
# ------- start -------
	a.save()
