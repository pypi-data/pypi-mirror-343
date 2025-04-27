#!venv/bin/pytest

import os
from confattr import ConfigFile, Config, MultiConfig, ConfigFileCommand, Message, NotificationLevel, state

import pytest
import _pytest
import pathlib

def pytest_configure(config: '_pytest.config.Config') -> None:
	if not getattr(config.option, 'template', None):
		config.option.template = ['html-dots/index.html']
	if not getattr(config.option, 'report', None):
		config.option.report = ['htmlpytest/report-%s.html' % os.environ.get('TOX_ENV', 'no-tox')]
	print("config.option.template", config.option.template)
	print("config.option.report", config.option.report)

@pytest.fixture(autouse=True)
def reset_config_path(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	assert ConfigFile.config_path is None
	assert ConfigFile.config_directory is None
	monkeypatch.setattr(ConfigFile, 'config_directory', str(tmp_path))
	monkeypatch.setattr(ConfigFileCommand, '_subclasses', ConfigFileCommand._subclasses.copy())
	monkeypatch.setattr(ConfigFileCommand, '_used_names', ConfigFileCommand._used_names.copy())
	monkeypatch.setattr(NotificationLevel, '_instances', NotificationLevel._instances.copy())
	monkeypatch.setattr(state, 'has_config_file_been_instantiated', False)
	monkeypatch.setattr(state, 'has_any_config_file_been_instantiated', False)
	Config.instances.clear()
	MultiConfig.reset()
	Message.reset()
