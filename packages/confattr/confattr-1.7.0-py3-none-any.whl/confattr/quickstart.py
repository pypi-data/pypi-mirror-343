#!./runmodule.sh

'''
Importing this module defines several settings which are useful in many applications and provides the :class:`~confattr.quickstart.ConfigManager` class.
This allows for an easy configuration setup in exchange for flexibility.
If you want more flexibility you can either subclass :class:`~confattr.quickstart.ConfigManager` and override specific methods or you do not import this module at all and use :class:`~confattr.configfile.ConfigFile` and :class:`~confattr.config.Config` directly.
'''

import sys
import argparse
from types import ModuleType
from collections.abc import Callable

from . import Config, ConfigFile, UiNotifier, Message, NotificationLevel
from .types import SubprocessCommandWithAlternatives as Command, OptionalExistingDirectory, TYPE_CONTEXT
from .utils import CallAction, HelpFormatter
from .configfile import Include, HelpWriter
from .formatters import List, Primitive


Include.home = Config('include.home', OptionalExistingDirectory(''), help="The directory where the include command looks for relative paths. An empty string is the default, the directory where the config file is located.")
Include.extensions = Config('include.extensions', [], help="File extensions to be suggested for auto completion of the include command. An empty list means all files with any extensions are suggested. The extensions should include the leading full stop. The check is case insensitive.", type=List(Primitive(str)))

class ConfigManager:

	#: A setting allowing the user to specify how to open text files, e.g. the config file
	editor = Config('editor', Command.editor(visual=False), help="The editor to be used when opening the config file.")

	#: A setting allowing the user to specify which messages they want to see when loading a config file with :meth:`~confattr.quickstart.ConfigManager.load`
	notification_level_config = Config('notification-level.config-file', NotificationLevel.ERROR)

	#: A setting allowing the user to specify which messages they want to see when parsing a line with :meth:`~confattr.quickstart.ConfigManager.parse_line`
	notification_level_ui = Config('notification-level.user-interface', NotificationLevel.INFO)

	#: Can be used to print messages to the user interface, uses :attr:`~confattr.quickstart.ConfigManager.notification_level_ui`
	ui_notifier: UiNotifier

	def __init__(self, appname: str, version: str, doc: 'str|None', *,
		changelog_url: 'str|None' = None,
		show_python_version_in_version: bool = False,
		show_additional_modules_in_version: 'list[ModuleType]' = [],
	) -> None:
		'''
		Defines two :class:`~confattr.configfile.ConfigFile` instances with separately configurable notification levels for :meth:`~confattr.quickstart.ConfigManager.load` and :meth:`~confattr.quickstart.ConfigManager.parse_line`.
		This object also provides :meth:`~confattr.quickstart.ConfigManager.create_argument_parser` to create an :class:`argparse.ArgumentParser` with commonly needed arguments.
		Note that all :class:`~confattr.config.Config` instances must be created before instantiating this class.

		:param appname: The name of the app, used to initialize :class:`~confattr.configfile.ConfigFile` and when printing the version number
		:param version: The version of the app, used when printing the version number
		:param doc: The package doc string, used as description when creating an :class:`~argparse.ArgumentParser`

		:param changelog_url: The URL to the change log, used when printing the version number
		:param show_additional_modules_in_version: A sequence of libraries which should be included when printing the version number
		:param show_python_version_in_version: If true: include the Python version number when printing the version number
		'''
		self.appname = appname
		self.version = version
		self.doc = doc
		self.changelog_url = changelog_url
		self.show_python_version_in_version = show_python_version_in_version
		self.show_additional_modules_in_version = show_additional_modules_in_version

		self.config_file = ConfigFile(appname=appname, notification_level=type(self).notification_level_config)
		self.user_interface = ConfigFile(appname=appname, notification_level=type(self).notification_level_ui, show_line_always=False)
		self.user_interface.command_dict['include'].config_file = self.config_file
		self.ui_notifier = self.user_interface.ui_notifier

	def set_ui_callback(self, callback: 'Callable[[Message], None]') -> None:
		'''
		Register a user interface notification callback function to all :class:`~confattr.configfile.ConfigFile` instances created by this object.

		See :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.
		'''
		self.config_file.set_ui_callback(callback)
		self.user_interface.set_ui_callback(callback)

	def print_errors_without_ui(self) -> None:
		'''
		Call :meth:`~confattr.quickstart.ConfigManager.set_ui_callback` with :func:`print` so that all messages are printed to the terminal.
		'''
		self.set_ui_callback(print)


	# ------- config file -------

	def load(self) -> bool:
		'''
		Load settings from config file and environment variables.

		:return: true if no errors have occurred, false if one or more errors have occurred
		'''
		return self.config_file.load()

	def parse_line(self, ln: str) -> bool:
		'''
		Parse a line from the user interface.

		:return: true if no errors have occurred, false if one or more errors have occurred
		'''
		return self.user_interface.parse_line(ln)

	def edit_config(self, *, context: TYPE_CONTEXT, update: bool = False) -> None:
		'''
		Open the config file in a text editor.

		If the config file does not exist it is created first.
		The text editor can be configured with :attr:`~confattr.quickstart.ConfigManager.editor`.

		:param context: Returns a context manager which can be used to stop and start an urwid screen.
		                It takes the command to be executed as argument so that it can log the command
		                and it returns the command to be executed so that it can modify the command,
		                e.g. processing and intercepting some environment variables.
		:param update: Load and rewrite the config file if it is already existing.
		'''
		if update:
			self.config_file.load()
		self.editor \
			.replace(Command.WC_FILE_NAME, self.config_file.save(if_not_existing=not update)) \
			.run(context=context)
		self.config_file.load()

	def get_save_path(self) -> str:
		'''
		:return: The first existing and writable file returned by :meth:`~confattr.configfile.ConfigFile.iter_config_paths` or the first path if none of the files are existing and writable.
		'''
		return self.config_file.get_save_path()

	def save(self, if_not_existing: bool = False) -> str:
		'''
		Save the current values of all settings to the file returned by :meth:`~confattr.configfile.ConfigFile.get_save_path`.
		Directories are created as necessary.

		:param if_not_existing: Do not overwrite the file if it is already existing.
		:return: The path to the file which has been written
		'''

		return self.config_file.save(if_not_existing=if_not_existing)


	# ------- creating an argument parser -------

	def create_argument_parser(self) -> argparse.ArgumentParser:
		'''
		Create an :class:`argparse.ArgumentParser` with arguments to display the version, edit the config file and choose a config file
		by calling :meth:`~confattr.quickstart.ConfigManager.create_empty_argument_parser`, :meth:`~confattr.quickstart.ConfigManager.add_config_help_argument`, :meth:`~confattr.quickstart.ConfigManager.add_version_argument` and :meth:`~confattr.quickstart.ConfigManager.add_config_related_arguments`.
		'''
		p = self.create_empty_argument_parser()
		self.add_config_help_argument(p)
		self.add_version_argument(p)
		self.add_config_related_arguments(p)
		return p

	def create_empty_argument_parser(self) -> argparse.ArgumentParser:
		'''
		Create an :class:`argparse.ArgumentParser` with the :paramref:`~confattr.quickstart.ConfigManager.doc` passed to the constructor as description and :class:`~confattr.utils.HelpFormatter` as formatter_class but without custom arguments.
		'''
		return argparse.ArgumentParser(description=self.doc, formatter_class=HelpFormatter)

	def add_config_help_argument(self, p: argparse.ArgumentParser) -> argparse.ArgumentParser:
		'''
		Add a ``--help-config`` argument to an :class:`argparse.ArgumentParser`.

		This is not part of :meth:`~confattr.quickstart.ConfigManager.add_config_related_arguments` so that this argument can be insterted between ``--help`` and ``--version``.

		:return: The same object that has been passed in
		'''
		p.add_argument('-H', '--help-config', action=CallAction, callback=self.print_config_help_and_exit)
		return p

	def add_version_argument(self, p: argparse.ArgumentParser) -> argparse.ArgumentParser:
		'''
		Add an argument to print the version and exit to an :class:`argparse.ArgumentParser`.

		:return: The same object that has been passed in
		'''
		p.add_argument('-v', '--version', action=CallAction, callback=self.print_version_and_exit)
		return p

	def add_config_related_arguments(self, p: argparse.ArgumentParser) -> argparse.ArgumentParser:
		'''
		Add arguments related to the config file to an :class:`argparse.ArgumentParser`.

		:return: The same object that has been passed in
		'''
		p.add_argument('-e', '--edit-config', action=CallAction, callback=self.edit_config_and_exit)
		p.add_argument('-E', '--update-and-edit-config', action=CallAction, callback=self.update_config_and_exit)
		p.add_argument('-c', '--config', action=CallAction, callback=self.select_config_file, nargs=1)
		return p


	# ------- printing version and help -------

	def print_version(self) -> None:
		versions: 'list[tuple[str, object]]' = []
		versions.append((self.appname, self.version))
		if self.show_python_version_in_version:
			versions.append(("python", sys.version))
		for mod in self.show_additional_modules_in_version:
			versions.append((mod.__name__, getattr(mod, '__version__', "(unknown version)")))

		for name, version in versions:
			print("%s %s" % (name, version))

		if self.changelog_url:
			print("change log:", self.changelog_url)

	def print_config_help(self) -> None:
		self.config_file.write_help(HelpWriter(sys.stdout))


	# ------- argument parser option callbacks -------

	def print_version_and_exit(self) -> None:
		'''show the version and exit'''
		self.print_version()
		sys.exit()

	def print_config_help_and_exit(self) -> None:
		'''show the config help and exit'''
		self.print_config_help()
		sys.exit()

	def edit_config_and_exit(self) -> None:
		'''edit the config file and exit'''
		self.edit_config(context=None, update=False)
		self.print_errors_without_ui()
		sys.exit()

	def update_config_and_exit(self) -> None:
		'''rewrite the config file, open it for editing and exit'''
		self.edit_config(context=None, update=True)
		self.print_errors_without_ui()
		sys.exit()

	def select_config_file(self, path: str) -> None:
		'''use this config file instead of the default'''
		ConfigFile.config_path = path
