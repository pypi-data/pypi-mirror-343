#!../../../../venv/bin/python3

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from confattr import ConfigFile
from map.example import Map

# ------- start -------
print(ConfigFile(appname='example').command_dict['map'].get_help())
