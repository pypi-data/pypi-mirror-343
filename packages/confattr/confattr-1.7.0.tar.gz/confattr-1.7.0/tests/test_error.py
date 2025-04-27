#!../venv/bin/pytest -s

import enum
import typing

import pytest

from confattr import Config, DictConfig, MultiConfig, MultiDictConfig, ConfigFile, ConfigId, ParseException, TimingError


def test_error_invalid_config_id() -> None:
	def check_config_id(config_id: ConfigId) -> None:
		if not config_id.endswith('car'):
			raise ParseException('only cars are supported')

	cf = ConfigFile(appname='test', check_config_id=check_config_id)
	with open(cf.get_save_path(), 'wt') as f:
		f.write('[my-bike]\n')
		f.write('[%s]\n' % Config.default_config_id)
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ['only cars are supported']

def test_error_set_multi_config_in_invalid_config_id() -> None:
	def check_config_id(config: 'MultiConfig[typing.Any]', config_id: ConfigId) -> None:
		if not config_id.endswith('car'):
			raise ParseException(f'{config.key} applies to cars only, not to {config_id!r}')

	MultiConfig('fuel', 'gasoline', check_config_id=check_config_id)

	cf = ConfigFile(appname='test')
	with open(cf.get_save_path(), 'wt') as f:
		f.write('''
set fuel = hydrogen

[alices-car]
set fuel = diesel

[bobs-bike]
set fuel = electricity
''')
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ["fuel applies to cars only, not to 'bobs-bike'"]

def test_error_set_multi_dict_config_in_invalid_config_id() -> None:
	def check_config_id(config: 'MultiConfig[typing.Any]', config_id: ConfigId) -> None:
		if not config_id.startswith('foo'):
			raise ParseException(f'invalid config id {config_id!r}')

	class Foo:

		color = MultiDictConfig('color', {'red': 242, 'green': 121, 'blue': 60}, unit='', check_config_id=check_config_id)

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	cf = ConfigFile(appname='test')
	with open(cf.get_save_path(), 'wt') as f:
		f.write('''
set color.red = 0

[foo]
set color.green = 0

[bar]
set color.blue = 0
''')
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ["invalid config id 'bar'"]

	foo = Foo('foo')
	assert foo.color['red']   ==   0
	assert foo.color['green'] ==   0
	assert foo.color['blue']  ==  60

	bar = Foo('bar')
	assert bar.color['red']   ==   0
	assert bar.color['green'] == 121
	assert bar.color['blue']  ==  60

	other = Foo('other')
	assert other.color['red']   ==   0
	assert other.color['green'] == 121
	assert other.color['blue']  ==  60



def test_error_sort_dict_config_by_enum_value_without_enum() -> None:
	class Month(enum.Enum):
		DECEMBER = 12
		JUNE = 6

	DictConfig('sunrise', {
		Month.DECEMBER: '8:17',
		6: '3:51',
	}, sort=DictConfig.Sort.ENUM_VALUE)

	with pytest.raises(TypeError, match="can only be used with enum keys"):
		cf = ConfigFile(appname='test')


def test_timing_error_if_defining_config_after_config_file() -> None:
	cf = ConfigFile(appname='test')

	with pytest.raises(TimingError):
		c = Config('too-late', True)

def test_timing_error_if_changing_keys_after_creating_a_config_file() -> None:
	c = Config('ok', True)
	cf = ConfigFile(appname='test')

	with pytest.raises(TimingError, match="ConfigFile has been instantiated already. Changing a key now would go unnoticed by that ConfigFile."):
		c.key = 'too-late'
