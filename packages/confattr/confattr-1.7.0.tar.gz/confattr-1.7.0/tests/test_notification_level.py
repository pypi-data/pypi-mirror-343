#!../venv/bin/pytest -s

import pytest

from confattr import Message, NotificationLevel, Config, ConfigFile


def test__custom_notification_level__less_important_than() -> None:
	WARNING = NotificationLevel.new('warning', less_important_than=NotificationLevel.ERROR)

	assert NotificationLevel.INFO < WARNING
	assert WARNING < NotificationLevel.ERROR

	assert NotificationLevel.ERROR > WARNING
	assert WARNING > NotificationLevel.INFO

	assert WARNING != NotificationLevel.ERROR
	assert WARNING != NotificationLevel.INFO

def test__custom_notification_level__more_important_than() -> None:
	WARNING = NotificationLevel.new('warning', more_important_than=NotificationLevel.INFO)

	assert NotificationLevel.INFO < WARNING
	assert WARNING < NotificationLevel.ERROR

	assert NotificationLevel.ERROR > WARNING
	assert WARNING > NotificationLevel.INFO

	assert WARNING != NotificationLevel.ERROR
	assert WARNING != NotificationLevel.INFO

def test__notification_level__no_duplicates() -> None:
	with pytest.warns(UserWarning):
		assert NotificationLevel.ERROR is NotificationLevel.new('error', more_important_than=NotificationLevel.INFO)

def test__notification_level__redefinition_with_wrong_more_important() -> None:
	with pytest.raises(ValueError, match="error is already defined and it's more important than info"):
		NotificationLevel.new('error', less_important_than=NotificationLevel.INFO)

def test__notification_level__redefinition_with_wrong_less_important() -> None:
	with pytest.raises(ValueError, match="info is already defined and it's less important than error"):
		NotificationLevel.new('info', more_important_than=NotificationLevel.ERROR)

def test__notification_level__importance_is_mandatory() -> None:
	with pytest.raises(TypeError, match="you must specify how important 'warning' is"):
		NotificationLevel.new('warning')

def test__notification_level__importance_is_mutually_exclusive() -> None:
	with pytest.raises(TypeError, match="more_important_than and less_important_than are mutually exclusive, you can only pass one of them"):
		NotificationLevel.new('warning', more_important_than=NotificationLevel.INFO, less_important_than=NotificationLevel.ERROR)

def test__notification_level__no_more_important_for_get() -> None:
	with pytest.raises(TypeError, match="more_important_than must not be passed when new = False"):
		NotificationLevel('error', more_important_than=NotificationLevel.INFO)

def test__notification_level__no_less_important_for_get() -> None:
	with pytest.raises(TypeError, match="less_important_than must not be passed when new = False"):
		NotificationLevel('info', less_important_than=NotificationLevel.ERROR)



def test__notification_level__get() -> None:
	assert NotificationLevel.ERROR is NotificationLevel.get('error')

def test__notification_level__constructor_returns_existing_instance() -> None:
	assert NotificationLevel.ERROR is NotificationLevel('error')

def test__notification_level__repr() -> None:
	assert repr(NotificationLevel.ERROR) == "NotificationLevel('error')"


def test__notification_level__config_file() -> None:
	nl = Config('status.notification-level', NotificationLevel.ERROR)
	cf = ConfigFile(appname='test', notification_level=nl)
	fn = cf.save()
	with open(fn, 'rt') as f:
		assert f.read() == """\
# status.notification-level
# -------------------------
# one of info, error
set status.notification-level = error
"""
