#!../venv/bin/pytest -vv

import os
import sys
import subprocess
import importlib
import typing
import pathlib
from dataclasses import dataclass
from collections.abc import Sequence, Mapping

import pytest

from confattr import Config, ConfigFile, Message, NotificationLevel, state
from confattr.quickstart import ConfigManager
import confattr.quickstart


# ------- utils ------

class MockRun:

	@dataclass
	class Call:
		__slots__ = ('cmd', 'kw')
		cmd: 'Sequence[str]'
		kw: 'Mapping[str, object]'

	def __init__(self) -> None:
		self.calls: 'list[MockRun.Call]' = []

	def __call__(self, cmds: 'Sequence[str]', **kw: 'typing.Any') -> None:
		self.calls.append(self.Call(
			cmd = cmds,
			kw = kw,
		))

	def __len__(self) -> int:
		return len(self.calls)

	def __getitem__(self, i: int) -> 'Call':
		return self.calls[i]

class MockUi:

	def __init__(self, cfg: ConfigManager) -> None:
		self.messages: 'list[Message]' = []
		cfg.set_ui_callback(self)

	def __call__(self, msg: Message) -> None:
		if msg.notification_level >= NotificationLevel.ERROR:
			self.messages.append(msg)

	def assert_no_errors(self) -> None:
		if self.messages:
			assert False, "errors have occurred:\n" + "\n".join(str(msg) for msg in self.messages)

	def assert_error(self, expected: str) -> None:
		if self.messages and expected in str(self.messages[0].message):
			self.messages = self.messages[1:]
			return
		assert False, "error %r has not occurred" % expected + "\n".join(str(msg) for msg in self.messages)

	def reset(self) -> None:
		self.messages.clear()

def read_file(fn: str) -> str:
	with open(fn, 'rt') as f:
		return f.read()

@pytest.fixture(autouse=True)
def ensure_config_instances_are_existing() -> None:
	if not Config.instances:
		importlib.reload(confattr.quickstart)


# ------- test command line options ------

def test_quickstart__version(capsys: 'pytest.CaptureFixture[str]') -> None:
	cfg = ConfigManager('test', '1.0.1', None)
	mockui = MockUi(cfg)
	p = cfg.create_argument_parser()
	p.add_argument('files', nargs='+')
	with pytest.raises(SystemExit):
		p.parse_args(['--version'])

	mockui.assert_no_errors()
	captured = capsys.readouterr()
	assert not captured.err
	assert captured.out == "test 1.0.1\n"

def test_quickstart__extended_version(capsys: 'pytest.CaptureFixture[str]') -> None:
	changelog_url = "https://mycoolapp.org/changelog"
	cfg = ConfigManager('test', '1.0.1', None,
		changelog_url = changelog_url,
		show_python_version_in_version = True,
		show_additional_modules_in_version = [pytest, os],
	)
	mockui = MockUi(cfg)
	p = cfg.create_argument_parser()
	p.add_argument('files', nargs='+')
	with pytest.raises(SystemExit):
		p.parse_args(['--version'])

	mockui.assert_no_errors()
	captured = capsys.readouterr()
	assert not captured.err
	assert captured.out == f"""\
test 1.0.1
python {sys.version}
pytest {pytest.__version__}
os (unknown version)
change log: {changelog_url}
"""

def test_quickstart__edit_config(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('EDITOR', 'myeditor')

	mock = MockRun()
	monkeypatch.setattr(subprocess, 'run', mock)

	cfg = ConfigManager('test', '1.0.1', None)
	mockui = MockUi(cfg)
	assert not os.path.isfile(cfg.get_save_path())

	p = cfg.create_argument_parser()
	p.add_argument('files', nargs='+')
	with pytest.raises(SystemExit):
		p.parse_args(['--edit'])

	mockui.assert_no_errors()
	assert len(mock) == 1
	assert mock[0].cmd == ['myeditor', cfg.get_save_path()]
	assert os.path.isfile(cfg.get_save_path())

def test_quickstart__update_config(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('EDITOR', 'myeditor')

	mock = MockRun()
	monkeypatch.setattr(subprocess, 'run', mock)

	c1 = Config('c1', "abc")
	cfg = ConfigManager('test', '1.0.1', None)
	mockui = MockUi(cfg)
	fn = cfg.save()
	state.has_config_file_been_instantiated = False

	c2 = Config('c2', "def")
	cfg = ConfigManager('test', '1.0.1', None)

	content = read_file(fn)
	assert 'c1' in content
	assert 'c2' not in content

	p = cfg.create_argument_parser()
	p.add_argument('files', nargs='+')
	with pytest.raises(SystemExit):
		p.parse_args(['--update-and-edit-config'])

	assert len(mock) == 1
	assert mock[0].cmd == ['myeditor', cfg.get_save_path()]
	assert os.path.isfile(cfg.get_save_path())

	content = read_file(fn)
	mockui.assert_no_errors()
	assert 'c1' in content
	assert 'c2' in content


def test_quickstart__other_config(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
	monkeypatch.setattr(ConfigFile, 'config_path', None)  # reset config_path at end of test which is set via --config

	c1 = Config('c1', "abc")
	c2 = Config('c2', "def")

	cfg = ConfigManager('test', '1.0.1', None)
	mockui = MockUi(cfg)

	fn = str(tmp_path / "tmp")
	with open(fn, 'wt') as f:
		f.write("set c1=ABC")

	p = cfg.create_argument_parser()
	p.add_argument('files', nargs='+')
	p.parse_args(['--config', fn, 'positional-argument'])

	cfg.load()
	mockui.assert_no_errors()
	assert c1.value == 'ABC'
	assert c2.value == 'def'


def test_quickstart__parse_line() -> None:
	c1 = Config('c1', "abc")
	c2 = Config('c2', "def")

	cfg = ConfigManager('test', '1.0.1', None)
	mockui = MockUi(cfg)
	cfg.parse_line("set c2 = DEF")

	mockui.assert_no_errors()
	assert c2.value == "DEF"
	assert c1.value == "abc"


def test_quickstart__include_home(tmp_path: 'pathlib.Path') -> None:
	c1 = Config('c1', "abc")
	tmp_path /= 'new'
	os.mkdir(tmp_path)

	with open(tmp_path / 'test-config', 'wt') as f:
		f.write('set c1 = "hello world"')

	cfg = ConfigManager('test', '1.0.1', None)
	assert os.path.dirname(cfg.get_save_path()) != str(tmp_path)
	mockui = MockUi(cfg)
	cfg.parse_line("include test-config")
	mockui.assert_error("no such file")
	assert c1.value == "abc"

	cfg.parse_line("set include.home=%r" % str(tmp_path))
	mockui.assert_no_errors()
	cfg.parse_line("include test-config")
	mockui.assert_no_errors()
	assert c1.value == "hello world"
