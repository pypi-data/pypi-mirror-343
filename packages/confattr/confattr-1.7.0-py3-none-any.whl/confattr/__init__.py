#!./runmodule.sh

'''
Config Attributes

A python library to read and write config files
with a syntax inspired by vimrc and ranger config.
'''

__version__ = '1.7.0'

from .config import Config, ExplicitConfig, DictConfig, MultiConfig, MultiDictConfig, ConfigId, TimingError
from .configfile import ConfigFile, NotificationLevel, Message, ParseException, MultipleParseExceptions, ConfigFileCommand, ConfigFileArgparseCommand, FormattedWriter, ConfigFileWriter, HelpWriter, SectionLevel, UiNotifier
from .formatters import Primitive, Hex, List, Set, Dict

try:
	from .configfile import SaveKwargs
except ImportError:  # pragma: no cover
	pass


__all__ = [
	# -------- for normal usage -------
	# imported from config
	'Config',
	'ExplicitConfig',
	'DictConfig',
	'MultiConfig',
	'MultiDictConfig',
	'ConfigId',
	# imported from configfile
	'ConfigFile',
	'NotificationLevel',
	'Message',
	'ParseException',
	'MultipleParseExceptions',
	'UiNotifier',
	# imported from formatters
	'Primitive',
	'Hex',
	'List',
	'Set',
	'Dict',
	## -------- for extending/customizing this package -------
	# imported from config
	'TimingError',
	# imported from configfile
	'SectionLevel',
	'FormattedWriter',
	'ConfigFileWriter',
	'HelpWriter',
	'SaveKwargs',
	'ConfigFileCommand',
	'ConfigFileArgparseCommand',
]
