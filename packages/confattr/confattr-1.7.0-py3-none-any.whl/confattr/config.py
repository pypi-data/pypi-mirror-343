#!./runmodule.sh

import builtins
import enum
import typing
from collections.abc import Iterable, Iterator, Container, Sequence, Mapping, Callable

if typing.TYPE_CHECKING:
	from typing_extensions import Self

from .formatters import AbstractFormatter, CopyableAbstractFormatter, Primitive, List, Set, Dict, format_primitive_value
from . import state


#: An identifier to specify which value of a :class:`~confattr.config.MultiConfig` or :class:`~confattr.config.MultiDictConfig` should be used for a certain object.
ConfigId = typing.NewType('ConfigId', str)

T_KEY = typing.TypeVar('T_KEY')
T = typing.TypeVar('T')
T_DEFAULT = typing.TypeVar('T_DEFAULT')

class TimingError(Exception):

	'''
	Is raised when trying to instantiate :class:`~confattr.config.Config` if a :class:`~confattr.configfile.ConfigFile` has been instantiated before without passing an explicit list or set to :paramref:`~confattr.configfile.ConfigFile.config_instances` or when trying to change a :attr:`~confattr.config.Config.key` after creating any :class:`~confattr.configfile.ConfigFile` because such changes would otherwise be silently ignored by that :class:`~confattr.configfile.ConfigFile`.
	'''


class Config(typing.Generic[T]):

	'''
	Each instance of this class represents a setting which can be changed in a config file.

	This class implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`__ to return :attr:`~confattr.config.Config.value` if an instance of this class is accessed as an instance attribute.
	If you want to get this object you need to access it as a class attribute.
	'''

	#: A mapping of all :class:`~confattr.config.Config` instances. The key in the mapping is the :attr:`~confattr.config.Config.key` attribute. The value is the :class:`~confattr.config.Config` instance. New :class:`~confattr.config.Config` instances add themselves automatically in their constructor.
	instances: 'dict[str, Config[typing.Any]]' = {}

	@classmethod
	def iter_instances(cls) -> 'Iterator[Config[typing.Any]|DictConfig[typing.Any, typing.Any]]':
		'''
		Yield the instances in :attr:`~confattr.config.Config.instances` but merge :class:`~confattr.config.DictConfig` items to a single :class:`~confattr.config.DictConfig` instance so that they can be sorted differently.
		'''
		parents = set()
		for cfg in cls.instances.values():
			if cfg.parent:
				if cfg.parent not in parents:
					yield cfg.parent
					parents.add(cfg.parent)
			else:
				yield cfg

	default_config_id = ConfigId('general')

	#: The value of this setting.
	value: 'T'

	#: Information about data type, unit and allowed values for :attr:`~confattr.config.Config.value` and methods how to parse, format and complete it.
	type: 'AbstractFormatter[T]'

	#: A description of this setting or a description for each allowed value.
	help: 'str|dict[T, str]|None'


	_key_changer: 'list[Callable[[str], str]]' = []

	@classmethod
	def push_key_changer(cls, callback: 'Callable[[str], str]') -> None:
		'''
		Modify the key of all settings which will be defined after calling this method.

		Call this before an ``import`` and :meth:`~confattr.config.Config.pop_key_changer` after it if you are unhappy with the keys of a third party library.
		If you import that library in different modules make sure you do this at the import which is executed first.

		:param callback: A function which takes the key as argument and returns the modified key.
		'''
		cls._key_changer.append(callback)

	@classmethod
	def pop_key_changer(cls) -> 'Callable[[str], str]':
		'''
		Undo the last call to :meth:`~confattr.config.Config.push_key_changer`.
		'''
		return cls._key_changer.pop()


	def __init__(self,
		key: str,
		default: T, *,
		type: 'AbstractFormatter[T]|None' = None,
		unit: 'str|None' = None,
		allowed_values: 'Sequence[T]|dict[str, T]|None' = None,
		help: 'str|dict[T, str]|None' = None,
		parent: 'DictConfig[typing.Any, T]|None' = None,
	):
		'''
		:param key: The name of this setting in the config file
		:param default: The default value of this setting
		:param type: How to parse, format and complete a value. Usually this is determined automatically based on :paramref:`~confattr.config.Config.default`. But if :paramref:`~confattr.config.Config.default` is an empty list the item type cannot be determined automatically so that this argument must be passed explicitly. This also gives the possibility to format a standard type differently e.g. as :class:`~confattr.formatters.Hex`. It is not permissible to reuse the same object for different settings, otherwise :meth:`AbstractFormatter.set_config_key() <confattr.formatters.AbstractFormatter.set_config_key>` will throw an exception.
		:param unit: The unit of an int or float value (only if type is None)
		:param allowed_values: The possible values this setting can have. Values read from a config file or an environment variable are checked against this. The :paramref:`~confattr.config.Config.default` value is *not* checked. (Only if type is None.)
		:param help: A description of this setting
		:param parent: Applies only if this is part of a :class:`~confattr.config.DictConfig`

		:obj:`~confattr.config.T` can be one of:
			* :class:`str`
			* :class:`int`
			* :class:`float`
			* :class:`bool`
			* a subclass of :class:`enum.Enum` (the value used in the config file is the name in lower case letters with hyphens instead of underscores)
			* a class where :meth:`~object.__str__` returns a string representation which can be passed to the constructor to create an equal object. \
			  A help which is written to the config file must be provided as a str in the class attribute :attr:`~confattr.types.AbstractType.help` or by adding it to :attr:`Primitive.help_dict <confattr.formatters.Primitive.help_dict>`. \
			  If that class has a str attribute :attr:`~confattr.types.AbstractType.type_name` this is used instead of the class name inside of config file.
			* a :class:`list` of any of the afore mentioned data types. The list may not be empty when it is passed to this constructor so that the item type can be derived but it can be emptied immediately afterwards. (The type of the items is not dynamically enforced—that's the job of a static type checker—but the type is mentioned in the help.)

		:raises ValueError: if key is not unique
		:raises TypeError: if :paramref:`~confattr.config.Config.default` is an empty list/set because the first element is used to infer the data type to which a value given in a config file is converted
		:raises TypeError: if this setting is a number or a list of numbers and :paramref:`~confattr.config.Config.unit` is not given
		:raises TimingError: if this setting is defined after creating a :class:`~confattr.configfile.ConfigFile` object without passing a list or set of settings to :paramref:`~confattr.configfile.ConfigFile.config_instances`
		'''
		if state.has_config_file_been_instantiated:
			raise TimingError("The setting %r is defined after instantiating a ConfigFile. It will not be available in the ConfigFile. If this is intentional you can avoid this Exception by explicitly passing a set or list of settings to config_instances of the ConfigFile." % key)
		if self._key_changer:
			key = self._key_changer[-1](key)

		if type is None:
			if isinstance(default, list):
				if not default:
					raise TypeError('I cannot infer the item type from an empty list. Please pass an argument to the type parameter.')
				item_type: 'builtins.type[T]' = builtins.type(default[0])
				type = typing.cast('AbstractFormatter[T]', List(item_type=Primitive(item_type, allowed_values=allowed_values, unit=unit)))
			elif isinstance(default, set):
				if not default:
					raise TypeError('I cannot infer the item type from an empty set. Please pass an argument to the type parameter.')
				item_type  = builtins.type(next(iter(default)))
				type = typing.cast('AbstractFormatter[T]', Set(item_type=Primitive(item_type, allowed_values=allowed_values, unit=unit)))
			elif isinstance(default, dict):
				if not default:
					raise TypeError('I cannot infer the key and value types from an empty dict. Please pass an argument to the type parameter.')
				some_key, some_value = next(iter(default.items()))
				key_type = Primitive(builtins.type(some_key))
				val_type = Primitive(builtins.type(some_value), allowed_values=allowed_values, unit=unit)
				type = typing.cast('AbstractFormatter[T]', Dict(key_type, val_type))
			else:
				type = Primitive(builtins.type(default), allowed_values=allowed_values, unit=unit)
		else:
			if unit is not None:
				raise TypeError("The keyword argument 'unit' is not supported if 'type' is given. Pass it to the type instead.")
			if allowed_values is not None:
				raise TypeError("The keyword argument 'allowed_values' is not supported if 'type' is given. Pass it to the type instead.")

		type.set_config_key(key)

		self._key = key
		self.value = default
		self.type = type
		self.help = help
		self.parent = parent

		cls = builtins.type(self)
		if key in cls.instances:
			raise ValueError(f'duplicate config key {key!r}')
		cls.instances[key] = self

	@property
	def key(self) -> str:
		'''
		The name of this setting which is used in the config file.
		This must be unique.
		You can change this attribute but only as long as no :class:`~confattr.configfile.ConfigFile` or :class:`~confattr.quickstart.ConfigManager` has been instantiated.
		'''
		return self._key

	@key.setter
	def key(self, key: str) -> None:
		if state.has_any_config_file_been_instantiated:
			raise TimingError('ConfigFile has been instantiated already. Changing a key now would go unnoticed by that ConfigFile.')
		if key in self.instances:
			raise ValueError(f'duplicate config key {key!r}')
		del self.instances[self._key]
		self._key = key
		self.type.config_key = key
		self.instances[key] = self


	@typing.overload
	def __get__(self, instance: None, owner: typing.Any = None) -> 'Self':
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> T:
		pass

	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'T|Self':
		if instance is None:
			return self

		return self.value

	def __set__(self: 'Config[T]', instance: typing.Any, value: T) -> None:
		self.value = value

	def __repr__(self) -> str:
		return '%s(%s, ...)' % (type(self).__name__, ', '.join(repr(a) for a in (self.key, self.value)))

	def set_value(self: 'Config[T]', config_id: 'ConfigId|None', value: T) -> None:
		'''
		This method is just to provide a common interface for :class:`~confattr.config.Config` and :class:`~confattr.config.MultiConfig`.
		If you know that you are dealing with a normal :class:`~confattr.config.Config` you can set :attr:`~confattr.config.Config.value` directly.
		'''
		if config_id is None:
			config_id = self.default_config_id
		if config_id != self.default_config_id:
			raise ValueError(f'{self.key} cannot be set for specific groups, config_id must be the default {self.default_config_id!r} not {config_id!r}')
		self.value = value

	def wants_to_be_exported(self) -> bool:
		return True

	def get_value(self, config_id: 'ConfigId|None') -> T:
		'''
		:return: :attr:`~confattr.config.Config.value`

		This getter is only to have a common interface for :class:`~confattr.config.Config` and :class:`~confattr.config.MultiConfig`
		'''
		return self.value

	def is_value_valid(self) -> bool:
		'''
		:return: true unless the value of an :class:`~confattr.config.ExplicitConfig` instance has not been set yet
		'''
		return True


class ExplicitConfig(Config[T]):

	'''
	A setting without a default value which requires the user to explicitly set a value in the config file or pass it as command line argument.

	You can use :meth:`~confattr.config.ExplicitConfig.is_value_valid` in order to check whether this config has a value or not.

	If you try to use the value before it has been set: If you try to access the config as instance attribute (:python:`object.config`) a :class:`TypeError` is thrown. Otherwise (:python:`config.value`) :obj:`None` is returned.
	'''

	def __init__(self,
		key: str,
		type: 'AbstractFormatter[T]|type[T]|None' = None, *,
		unit: 'str|None' = None,
		allowed_values: 'Sequence[T]|dict[str, T]|None' = None,
		help: 'str|dict[T, str]|None' = None,
		parent: 'DictConfig[typing.Any, T]|None' = None,
	):
		'''
		:param key: The name of this setting in the config file
		:param type: How to parse, format and complete a value. Any class which can be passed to :class:`~confattr.formatters.Primitive` or an object of a subclass of :class:`~confattr.formatters.AbstractFormatter`.
		:param unit: The unit of an int or float value (only if type is not an :class:`~confattr.formatters.AbstractFormatter`)
		:param allowed_values: The possible values this setting can have. Values read from a config file or an environment variable are checked against this. The :paramref:`~confattr.config.Config.default` value is *not* checked. (Only if type is not an :class:`~confattr.formatters.AbstractFormatter`.)
		:param help: A description of this setting
		:param parent: Applies only if this is part of a :class:`~confattr.config.DictConfig`
		'''
		if type is None:
			if not allowed_values:
				raise TypeError("missing required positional argument: 'type'")
			elif isinstance(allowed_values, dict):
				type = builtins.type(tuple(allowed_values.values())[0])
			else:
				type = builtins.type(allowed_values[0])
		if not isinstance(type, AbstractFormatter):
			type = Primitive(type, unit=unit, allowed_values=allowed_values)
		super().__init__(key,
			default = None,  # type: ignore [arg-type]
			type = type,
			help = help,
			parent = parent,
		)

	@typing.overload
	def __get__(self, instance: None, owner: typing.Any = None) -> 'Self':
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> T:
		pass

	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'T|Self':
		if instance is None:
			return self

		if self.value is None:
			raise TypeError(f"value for {self.key!r} has not been set")
		return self.value

	def is_value_valid(self) -> bool:
		return self.value is not None


class DictConfig(typing.Generic[T_KEY, T]):

	'''
	A container for several settings which belong together.
	Except for :meth:`~object.__eq__` and :meth:`~object.__ne__` it behaves like a normal :class:`~collections.abc.Mapping`
	but internally the items are stored in :class:`~confattr.config.Config` instances.

	In contrast to a :class:`~confattr.config.Config` instance it does *not* make a difference whether an instance of this class is accessed as a type or instance attribute.
	'''

	class Sort(enum.Enum):
		NAME = enum.auto()
		ENUM_VALUE = enum.auto()
		NONE = enum.auto()

	def __init__(self,
		key_prefix: str,
		default_values: 'dict[T_KEY, T]', *,
		type: 'CopyableAbstractFormatter[T]|None' = None,
		ignore_keys: 'Container[T_KEY]' = set(),
		unit: 'str|None' = None,
		allowed_values: 'Sequence[T]|dict[str, T]|None' = None,
		help: 'str|None' = None,
		sort: Sort = Sort.NAME,
	) -> None:
		'''
		:param key_prefix: A common prefix which is used by :meth:`~confattr.config.DictConfig.format_key` to generate the :attr:`~confattr.config.Config.key` by which the setting is identified in the config file
		:param default_values: The content of this container. A :class:`~confattr.config.Config` instance is created for each of these values (except if the key is contained in :paramref:`~confattr.config.DictConfig.ignore_keys`). See :meth:`~confattr.config.DictConfig.format_key`.
		:param type: How to parse, format and complete a value. Usually this is determined automatically based on :paramref:`~confattr.config.DictConfig.default_values`. But if you want more control you can implement your own class and pass it to this parameter.
		:param ignore_keys: All items which have one of these keys are *not* stored in a :class:`~confattr.config.Config` instance, i.e. cannot be set in the config file.
		:param unit: The unit of all items (only if type is None)
		:param allowed_values: The possible values these settings can have. Values read from a config file or an environment variable are checked against this. The :paramref:`~confattr.config.DictConfig.default_values` are *not* checked. (Only if type is None.)
		:param help: A help for all items
		:param sort: How to sort the items of this dictionary in the config file/documentation

		:raises ValueError: if a key is not unique
		'''
		self._values: 'dict[T_KEY, Config[T]]' = {}
		self._ignored_values: 'dict[T_KEY, T]' = {}
		self.allowed_values = allowed_values
		self.sort = sort

		self.key_prefix = key_prefix
		self.key_changer = Config._key_changer[-1] if Config._key_changer else lambda key: key
		self.type = type
		self.unit = unit
		self.help = help
		self.ignore_keys = ignore_keys

		for key, val in default_values.items():
			self[key] = val

	def format_key(self, key: T_KEY) -> str:
		'''
		Generate a key by which the setting can be identified in the config file based on the dict key by which the value is accessed in the python code.

		:return: :paramref:`~confattr.config.DictConfig.key_prefix` + dot + :paramref:`~confattr.config.DictConfig.format_key.key`
		'''
		key_str = format_primitive_value(key)
		return '%s.%s' % (self.key_prefix, key_str)

	def __setitem__(self: 'DictConfig[T_KEY, T]', key: T_KEY, val: T) -> None:
		if key in self.ignore_keys:
			self._ignored_values[key] = val
			return

		c = self._values.get(key)
		if c is None:
			self._values[key] = self.new_config(self.format_key(key), val, unit=self.unit, help=self.help)
		else:
			c.value = val

	def new_config(self: 'DictConfig[T_KEY, T]', key: str, default: T, *, unit: 'str|None', help: 'str|dict[T, str]|None') -> Config[T]:
		'''
		Create a new :class:`~confattr.config.Config` instance to be used internally
		'''
		return Config(key, default, type=self.type.copy() if self.type else None, unit=unit, help=help, parent=self, allowed_values=self.allowed_values)

	def __getitem__(self, key: T_KEY) -> T:
		if key in self.ignore_keys:
			return self._ignored_values[key]
		else:
			return self._values[key].value

	@typing.overload
	def get(self, key: T_KEY) -> 'T|None':
		...

	@typing.overload
	def get(self, key: T_KEY, default: T_DEFAULT) -> 'T|T_DEFAULT':
		...

	def get(self, key: T_KEY, default: 'typing.Any' = None) -> 'typing.Any':
		try:
			return self[key]
		except KeyError:
			return default

	def __repr__(self) -> str:
		values = {key:val.value for key,val in self._values.items()}
		values.update({key:val for key,val in self._ignored_values.items()})
		return '%s(%r, ignore_keys=%r, ...)' % (type(self).__name__, values, self.ignore_keys)

	def __contains__(self, key: T_KEY) -> bool:
		if key in self.ignore_keys:
			return key in self._ignored_values
		else:
			return key in self._values

	def __iter__(self) -> 'Iterator[T_KEY]':
		yield from self._values
		yield from self._ignored_values

	def keys(self) -> 'Iterator[T_KEY]':
		yield from self._values.keys()
		yield from self._ignored_values.keys()

	def values(self) -> 'Iterator[T]':
		for cfg in self._values.values():
			yield cfg.value
		yield from self._ignored_values.values()

	def items(self) -> 'Iterator[tuple[T_KEY, T]]':
		for key, cfg in self._values.items():
			yield key, cfg.value
		yield from self._ignored_values.items()


	def iter_configs(self) -> 'Iterator[Config[T]]':
		'''
		Iterate over the :class:`~confattr.config.Config` instances contained in this dict,
		sorted by the argument passed to :paramref:`~confattr.config.DictConfig.sort` in the constructor
		'''
		if self.sort is self.Sort.NAME:
			yield from sorted(self._values.values(), key=lambda c: c.key)
		elif self.sort is self.Sort.NONE:
			yield from self._values.values()
		elif self.sort is self.Sort.ENUM_VALUE:
			#keys = typing.cast('Iterable[enum.Enum]', self._values.keys())
			#keys = tuple(self._values)
			if is_mapping_with_enum_keys(self._values):
				for key in sorted(self._values.keys(), key=lambda c: c.value):
					yield self._values[key]
			else:
				raise TypeError("%r can only be used with enum keys" % self.sort)
		else:
			raise NotImplementedError("sort %r is not implemented" % self.sort)

def is_mapping_with_enum_keys(m: 'Mapping[typing.Any, T]') -> 'typing.TypeGuard[Mapping[enum.Enum, T]]':
	return all(isinstance(key, enum.Enum) for key in m.keys())


# ========== settings which can have different values for different groups ==========

class MultiConfig(Config[T]):

	'''
	A setting which can have different values for different objects.

	This class implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`__ to return one of the values in :attr:`~confattr.config.MultiConfig.values` depending on a ``config_id`` attribute of the owning object if an instance of this class is accessed as an instance attribute.
	If there is no value for the ``config_id`` in :attr:`~confattr.config.MultiConfig.values` :attr:`~confattr.config.MultiConfig.value` is returned instead.
	If the owning instance does not have a ``config_id`` attribute an :class:`AttributeError` is raised.

	In the config file a group can be opened with ``[config-id]``.
	Then all following ``set`` commands set the value for the specified config id.
	'''

	#: A list of all config ids for which a value has been set in any instance of this class (regardless of via code or in a config file and regardless of whether the value has been deleted later on). This list is cleared by :meth:`~confattr.config.MultiConfig.reset`.
	config_ids: 'list[ConfigId]' = []

	#: Stores the values for specific objects.
	values: 'dict[ConfigId, T]'

	#: Stores the default value which is used if no value for the object is defined in :attr:`~confattr.config.MultiConfig.values`.
	value: 'T'

	#: The callable which has been passed to the constructor as :paramref:`~confattr.config.MultiConfig.check_config_id`
	check_config_id: 'Callable[[MultiConfig[T], ConfigId], None]|None'

	@classmethod
	def reset(cls) -> None:
		'''
		Clear :attr:`~confattr.config.MultiConfig.config_ids` and clear :attr:`~confattr.config.MultiConfig.values` for all instances in :attr:`Config.instances <confattr.config.Config.instances>`
		'''
		cls.config_ids.clear()
		for cfg in Config.instances.values():
			if isinstance(cfg, MultiConfig):
				cfg.values.clear()

	def __init__(self,
		key: str,
		default: T, *,
		type: 'AbstractFormatter[T]|None' = None,
		unit: 'str|None' = None,
		allowed_values: 'Sequence[T]|dict[str, T]|None' = None,
		help: 'str|dict[T, str]|None' = None,
		parent: 'MultiDictConfig[typing.Any, T]|None' = None,
		check_config_id: 'Callable[[MultiConfig[T], ConfigId], None]|None' = None,
	) -> None:
		'''
		:param key: The name of this setting in the config file
		:param default: The default value of this setting
		:param help: A description of this setting
		:param type: How to parse, format and complete a value. Usually this is determined automatically based on :paramref:`~confattr.config.MultiConfig.default`. But if :paramref:`~confattr.config.MultiConfig.default` is an empty list the item type cannot be determined automatically so that this argument must be passed explicitly. This also gives the possibility to format a standard type differently e.g. as :class:`~confattr.formatters.Hex`. It is not permissible to reuse the same object for different settings, otherwise :meth:`AbstractFormatter.set_config_key() <confattr.formatters.AbstractFormatter.set_config_key>` will throw an exception.
		:param unit: The unit of an int or float value (only if type is None)
		:param allowed_values: The possible values this setting can have. Values read from a config file or an environment variable are checked against this. The :paramref:`~confattr.config.MultiConfig.default` value is *not* checked. (Only if type is None.)
		:param parent: Applies only if this is part of a :class:`~confattr.config.MultiDictConfig`
		:param check_config_id: Is called every time a value is set in the config file (except if the config id is :attr:`~confattr.config.Config.default_config_id`—that is always allowed). The callback should raise a :class:`~confattr.configfile.ParseException` if the config id is invalid.
		'''
		super().__init__(key, default, type=type, unit=unit, help=help, parent=parent, allowed_values=allowed_values)
		self.values: 'dict[ConfigId, T]' = {}
		self.check_config_id = check_config_id

	# I don't know why this code duplication is necessary,
	# I have declared the overloads in the parent class already.
	# But without copy-pasting this code mypy complains
	# "Signature of __get__ incompatible with supertype Config"
	@typing.overload
	def __get__(self, instance: None, owner: typing.Any = None) -> 'Self':
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> T:
		pass

	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'T|Self':
		if instance is None:
			return self

		return self.values.get(instance.config_id, self.value)

	def __set__(self: 'MultiConfig[T]', instance: typing.Any, value: T) -> None:
		config_id = instance.config_id
		self.values[config_id] = value
		if config_id not in self.config_ids:
			self.config_ids.append(config_id)

	def set_value(self: 'MultiConfig[T]', config_id: 'ConfigId|None', value: T) -> None:
		'''
		Check :paramref:`~confattr.config.MultiConfig.set_value.config_id` by calling :meth:`~confattr.config.MultiConfig.check_config_id` and
		set the value for the object(s) identified by :paramref:`~confattr.config.MultiConfig.set_value.config_id`.

		If you know that :paramref:`~confattr.config.MultiConfig.set_value.config_id` is valid you can also change the items of :attr:`~confattr.config.MultiConfig.values` directly.
		That is especially useful in test automation with :meth:`pytest.MonkeyPatch.setitem`.

		If you want to set the default value you can also set :attr:`~confattr.config.MultiConfig.value` directly.

		:param config_id: Identifies the object(s) for which :paramref:`~confattr.config.MultiConfig.set_value.value` is intended. :obj:`None` is equivalent to :attr:`~confattr.config.MultiConfig.default_config_id`.
		:param value: The value to be assigned for the object(s) identified by :paramref:`~confattr.config.MultiConfig.set_value.config_id`.
		'''
		if config_id is None:
			config_id = self.default_config_id
		if self.check_config_id and config_id != self.default_config_id:
			self.check_config_id(self, config_id)
		if config_id == self.default_config_id:
			self.value = value
		else:
			self.values[config_id] = value
		if config_id not in self.config_ids:
			self.config_ids.append(config_id)

	def get_value(self, config_id: 'ConfigId|None') -> T:
		'''
		:return: The corresponding value from :attr:`~confattr.config.MultiConfig.values` if :paramref:`~confattr.config.MultiConfig.get_value.config_id` is contained or :attr:`~confattr.config.MultiConfig.value` otherwise
		'''
		if config_id is None:
			config_id = self.default_config_id
		return self.values.get(config_id, self.value)


class MultiDictConfig(DictConfig[T_KEY, T]):

	'''
	A container for several settings which can have different values for different objects.

	This is essentially a :class:`~confattr.config.DictConfig` using :class:`~confattr.config.MultiConfig` instead of normal :class:`~confattr.config.Config`.
	However, in order to return different values depending on the ``config_id`` of the owning instance, it implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`__ to return an :class:`~confattr.config.InstanceSpecificDictMultiConfig` if it is accessed as an instance attribute.
	'''

	def __init__(self,
		key_prefix: str,
		default_values: 'dict[T_KEY, T]', *,
		type: 'CopyableAbstractFormatter[T]|None' = None,
		ignore_keys: 'Container[T_KEY]' = set(),
		unit: 'str|None' = None,
		allowed_values: 'Sequence[T]|dict[str, T]|None' = None,
		help: 'str|None' = None,
		check_config_id: 'Callable[[MultiConfig[T], ConfigId], None]|None' = None,
	) -> None:
		'''
		:param key_prefix: A common prefix which is used by :meth:`~confattr.config.MultiDictConfig.format_key` to generate the :attr:`~confattr.config.Config.key` by which the setting is identified in the config file
		:param default_values: The content of this container. A :class:`~confattr.config.Config` instance is created for each of these values (except if the key is contained in :paramref:`~confattr.config.MultiDictConfig.ignore_keys`). See :meth:`~confattr.config.MultiDictConfig.format_key`.
		:param type: How to parse, format and complete a value. Usually this is determined automatically based on :paramref:`~confattr.config.MultiDictConfig.default_values`. But if you want more control you can implement your own class and pass it to this parameter.
		:param ignore_keys: All items which have one of these keys are *not* stored in a :class:`~confattr.config.Config` instance, i.e. cannot be set in the config file.
		:param unit: The unit of all items (only if type is None)
		:param allowed_values: The possible values these settings can have. Values read from a config file or an environment variable are checked against this. The :paramref:`~confattr.config.MultiDictConfig.default_values` are *not* checked. (Only if type is None.)
		:param help: A help for all items
		:param check_config_id: Is passed through to :class:`~confattr.config.MultiConfig`

		:raises ValueError: if a key is not unique
		'''
		self.check_config_id = check_config_id
		super().__init__(
			key_prefix = key_prefix,
			default_values = default_values,
			type = type,
			ignore_keys = ignore_keys,
			unit = unit,
			help = help,
			allowed_values = allowed_values,
		)

	@typing.overload
	def __get__(self, instance: None, owner: typing.Any = None) -> 'Self':
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'InstanceSpecificDictMultiConfig[T_KEY, T]':
		pass

	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'InstanceSpecificDictMultiConfig[T_KEY, T]|Self':
		if instance is None:
			return self

		return InstanceSpecificDictMultiConfig(self, instance.config_id)

	def __set__(self: 'MultiDictConfig[T_KEY, T]', instance: typing.Any, value: 'InstanceSpecificDictMultiConfig[T_KEY, T]') -> typing.NoReturn:
		raise NotImplementedError()

	def new_config(self: 'MultiDictConfig[T_KEY, T]', key: str, default: T, *, unit: 'str|None', help: 'str|dict[T, str]|None') -> MultiConfig[T]:
		return MultiConfig(key, default, type=self.type.copy() if self.type else None, unit=unit, help=help, parent=self, allowed_values=self.allowed_values, check_config_id=self.check_config_id)

class InstanceSpecificDictMultiConfig(typing.Generic[T_KEY, T]):

	'''
	An intermediate instance which is returned when accsessing
	a :class:`~confattr.config.MultiDictConfig` as an instance attribute.
	Can be indexed like a normal :class:`dict`.
	'''

	def __init__(self, mdc: 'MultiDictConfig[T_KEY, T]', config_id: ConfigId) -> None:
		self.mdc = mdc
		self.config_id = config_id

	def __setitem__(self: 'InstanceSpecificDictMultiConfig[T_KEY, T]', key: T_KEY, val: T) -> None:
		if key in self.mdc.ignore_keys:
			raise TypeError('cannot set value of ignored key %r' % key)

		c = self.mdc._values.get(key)
		if c is None:
			self.mdc._values[key] = MultiConfig(self.mdc.format_key(key), val, help=self.mdc.help)
		else:
			c.__set__(self, val)

	def __getitem__(self, key: T_KEY) -> T:
		if key in self.mdc.ignore_keys:
			return self.mdc._ignored_values[key]
		else:
			return self.mdc._values[key].__get__(self)
