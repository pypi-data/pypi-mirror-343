#!../venv/bin/pytest -vv

from confattr import NotificationLevel, ConfigFile, Message, Config
from confattr.configfile import UiNotifier
from confattr.utils import HelpFormatter, HelpFormatterWrapper, SortedEnum, CallAction

import sys
import argparse
import pytest

# ------- SortedEnum -------

def test__sorted_enum__cmp__ascending() -> None:
	class Level(SortedEnum):
		ONE = 'one'
		TWO = 'two'

	# ----- different -----
	assert Level.TWO > Level.ONE
	assert Level.TWO >= Level.ONE
	assert Level.TWO != Level.ONE  # type: ignore [comparison-overlap]

	assert not Level.TWO < Level.ONE
	assert not Level.TWO <= Level.ONE
	assert not Level.TWO == Level.ONE  # type: ignore [comparison-overlap]
	assert not Level.TWO is Level.ONE  # type: ignore [comparison-overlap]

	# ----- same -----
	assert not Level.ONE > Level.ONE
	assert not Level.ONE < Level.ONE
	assert not Level.ONE != Level.ONE

	assert Level.ONE <= Level.ONE
	assert Level.ONE >= Level.ONE
	assert Level.ONE == Level.ONE
	assert Level.ONE is Level.ONE

@pytest.mark.skipif(sys.version_info < (3, 10), reason="passing a class argument to a subclass of enum.Enum requires python v3.10.0a4 or higher")
def test__sorted_enum__cmp__descending() -> None:
	class Level(SortedEnum, descending=True):
		TWO = 'two'
		ONE = 'one'

	# ----- different -----
	assert Level.TWO > Level.ONE
	assert Level.TWO >= Level.ONE
	assert Level.TWO != Level.ONE  # type: ignore [comparison-overlap]

	assert not Level.TWO < Level.ONE
	assert not Level.TWO <= Level.ONE
	assert not Level.TWO == Level.ONE  # type: ignore [comparison-overlap]
	assert not Level.TWO is Level.ONE  # type: ignore [comparison-overlap]

	# ----- same -----
	assert not Level.ONE > Level.ONE
	assert not Level.ONE < Level.ONE
	assert not Level.ONE != Level.ONE

	assert Level.ONE <= Level.ONE
	assert Level.ONE >= Level.ONE
	assert Level.ONE == Level.ONE
	assert Level.ONE is Level.ONE


def test__sorted_enum__add__ascending() -> None:
	class Level(SortedEnum):
		ONE = 'one'
		TWO = 'two'
		THREE = 'three'
		FOUR = 'four'

	# ----- in boundaries -----
	assert Level.TWO + 1 is Level.THREE
	assert Level.TWO - 1 is Level.ONE
	assert Level.ONE + 3 is Level.FOUR
	assert Level.FOUR - 2 is Level.TWO

	# ----- limit -----
	assert Level.ONE - 1 is Level.ONE
	assert Level.TWO - 4 is Level.ONE

	assert Level.FOUR + 1 is Level.FOUR
	assert Level.TWO + 8 is Level.FOUR

@pytest.mark.skipif(sys.version_info < (3, 10), reason="passing a class argument to a subclass of enum.Enum requires python v3.10.0a4 or higher")
def test__sorted_enum__add__descending() -> None:
	class Level(SortedEnum, descending=True):
		FOUR = 'four'
		THREE = 'three'
		TWO = 'two'
		ONE = 'one'

	# ----- in boundaries -----
	assert Level.TWO + 1 is Level.THREE
	assert Level.TWO - 1 is Level.ONE
	assert Level.ONE + 3 is Level.FOUR
	assert Level.FOUR - 2 is Level.TWO

	# ----- limit -----
	assert Level.ONE - 1 is Level.ONE
	assert Level.TWO - 4 is Level.ONE

	assert Level.FOUR + 1 is Level.FOUR
	assert Level.TWO + 8 is Level.FOUR


# ------- NotificationLevel -------

def test__notification_level__compare_different() -> None:
	assert NotificationLevel.ERROR > NotificationLevel.INFO
	assert NotificationLevel.ERROR >= NotificationLevel.INFO
	assert NotificationLevel.ERROR != NotificationLevel.INFO

	assert not NotificationLevel.ERROR < NotificationLevel.INFO
	assert not NotificationLevel.ERROR <= NotificationLevel.INFO
	assert not NotificationLevel.ERROR == NotificationLevel.INFO
	assert not NotificationLevel.ERROR is NotificationLevel.INFO

def test__notification_level__compare_same() -> None:
	assert not NotificationLevel.INFO > NotificationLevel.INFO
	assert not NotificationLevel.INFO < NotificationLevel.INFO
	assert not NotificationLevel.INFO != NotificationLevel.INFO

	assert NotificationLevel.INFO <= NotificationLevel.INFO
	assert NotificationLevel.INFO >= NotificationLevel.INFO
	assert NotificationLevel.INFO == NotificationLevel.INFO
	assert NotificationLevel.INFO is NotificationLevel.INFO


# ------- UiNotifier -------

class MockUI:

	def __init__(self) -> None:
		self.messages: 'list[tuple[NotificationLevel, str|BaseException]]' = []

	def reset(self) -> None:
		self.messages.clear()

	def show(self, msg: Message) -> None:
		self.messages.append((msg.notification_level, msg.format_msg_line()))


def test__ui_notifier__notification_level_info() -> None:
	ui_notifier = UiNotifier(config_file=ConfigFile(appname='test'), notification_level=NotificationLevel.INFO)
	ui = MockUI()
	ui_notifier.set_ui_callback(ui.show)

	ui.reset()
	ui_notifier.show_error('boom')
	assert ui.messages == [(NotificationLevel.ERROR, 'boom')]

	ui.reset()
	ui_notifier.show_info('fyi')
	assert ui.messages == [(NotificationLevel.INFO, 'fyi')]

def test__ui_notifier__notification_level_error() -> None:
	ui_notifier = UiNotifier(config_file=ConfigFile(appname='test'), notification_level=NotificationLevel.ERROR)
	ui = MockUI()
	ui_notifier.set_ui_callback(ui.show)

	ui.reset()
	ui_notifier.show_error('boom')
	assert ui.messages == [(NotificationLevel.ERROR, 'boom')]

	ui.reset()
	ui_notifier.show_info('fyi')
	assert ui.messages == []


def test__ui_notifier__store_messages() -> None:
	ui_notifier = UiNotifier(config_file=ConfigFile(appname='test'))

	ui_notifier.show_info('info 1')
	ui_notifier.show_error('error 1')
	ui_notifier.notification_level = NotificationLevel.INFO
	ui_notifier.show_error('error 2')
	ui_notifier.show_info('info 2')

	ui = MockUI()
	ui_notifier.set_ui_callback(ui.show)
	assert ui.messages == [
		(NotificationLevel.ERROR, 'error 1'),
		(NotificationLevel.ERROR, 'error 2'),
		(NotificationLevel.INFO, 'info 2'),
	]

def test__ui_notifier__change_notification_level_config() -> None:
	config_file = ConfigFile(appname='test', notification_level=Config('notification-level', NotificationLevel.ERROR))
	config_file.save()
	ui_notifier = config_file.ui_notifier

	ui_notifier.show_info('info 1')
	ui_notifier.show_error('error 1')
	ui_notifier.notification_level = NotificationLevel.INFO
	ui_notifier.show_info('info 2')
	ui_notifier.show_error('error 2')
	config_file.load()
	ui_notifier.show_info('info 3')
	ui_notifier.show_error('error 3')

	ui = MockUI()
	ui_notifier.set_ui_callback(ui.show)
	assert ui.messages == [
		(NotificationLevel.ERROR, 'error 1'),
		(NotificationLevel.INFO, 'info 2'),
		(NotificationLevel.ERROR, 'error 2'),
		(NotificationLevel.ERROR, 'error 3'),
	]


# ------- custom argparse HelpFormatter -------

def test__help_formatter__empty_string() -> None:
	raw = ''
	expected = ''
	assert HelpFormatter('prog')._fill_text(raw, width=20, indent='') == expected

def test__help_formatter__strip_indentation_and_merge_lines() -> None:
	raw = '''
		abc
		def
		ghi
	'''
	expected = 'abc def ghi'

	assert HelpFormatter('prog')._fill_text(raw, width=20, indent='') == expected

def test__help_formatter__strip_indentation_2() -> None:
	raw = '''\
		abc
		def
		ghi
	'''
	expected = 'abc def ghi'

	assert HelpFormatter('prog')._fill_text(raw, width=20, indent='') == expected

def test__help_formatter__wrap_lines() -> None:
	raw = '''
	The quick brown fox jumps over the lazy dog.
	Waltz, bad nymph, for quick jigs vex.
	Sphinx of black quartz, judge my vow.
	How vexingly quick daft zebras jump!
	'''
	expected = '''\
The quick brown fox jumps over the lazy dog. Waltz, bad
nymph, for quick jigs vex. Sphinx of black quartz, judge my
vow. How vexingly quick daft zebras jump!'''

	width = 60
	out = HelpFormatter('prog')._fill_text(raw, width=width, indent='')
	for ln in out.splitlines():
		assert len(ln) <= width

	assert out == expected

def test__help_formatter__keep_paragraphs() -> None:
	raw = '''
	The quick brown fox jumps over the lazy dog.
	Waltz, bad nymph, for quick jigs vex.

	Sphinx of black quartz, judge my vow.
	How vexingly quick daft zebras jump!
	'''
	expected = '''\
The quick brown fox jumps over the lazy
dog. Waltz, bad nymph, for quick jigs
vex.

Sphinx of black quartz, judge my vow.
How vexingly quick daft zebras jump!'''

	width = 40
	out = HelpFormatter('prog')._fill_text(raw, width=width, indent='')
	for ln in out.splitlines():
		assert len(ln) <= width

	assert out == expected

def test__help_formatter__two_empty_lines_are_equivalent_to_one() -> None:
	raw = '''
	The quick brown fox jumps over the lazy dog.
	Waltz, bad nymph, for quick jigs vex.


	Sphinx of black quartz, judge my vow.
	How vexingly quick daft zebras jump!
	'''
	expected = '''\
The quick brown fox jumps over the lazy
dog. Waltz, bad nymph, for quick jigs
vex.

Sphinx of black quartz, judge my vow.
How vexingly quick daft zebras jump!'''

	width = 40
	out = HelpFormatter('prog')._fill_text(raw, width=width, indent='')
	for ln in out.splitlines():
		assert len(ln) <= width

	assert out == expected

def test__help_formatter__dont_break_urls() -> None:
	raw = '''
	The quick brown fox jumps over the lazy dog.
	Waltz, bad nymph, for quick jigs vex.

	https://mikeyanderson.com/optimal_characters_per_line

	Sphinx of black quartz, judge my vow.
	How vexingly quick daft zebras jump!
	'''
	expected = '''\
The quick brown fox jumps over
the lazy dog. Waltz, bad
nymph, for quick jigs vex.

https://mikeyanderson.com/optimal_characters_per_line

Sphinx of black quartz, judge
my vow. How vexingly quick
daft zebras jump!'''

	out = HelpFormatter('prog')._fill_text(raw, width=30, indent='')
	assert out == expected

def test__help_formatter__indent() -> None:
	raw = '''
	The quick brown fox jumps over the lazy dog.
	Waltz, bad nymph, for quick jigs vex.

	https://mikeyanderson.com/optimal_characters_per_line

	Sphinx of black quartz, judge my vow.
	How vexingly quick daft zebras jump!
	'''
	expected = '''\
        | The quick brown fox
        | jumps over the lazy
        | dog. Waltz, bad
        | nymph, for quick
        | jigs vex.

        | https://mikeyanderson.com/optimal_characters_per_line

        | Sphinx of black
        | quartz, judge my
        | vow. How vexingly
        | quick daft zebras
        | jump!'''

	out = HelpFormatter('prog')._fill_text(raw, width=30, indent='        | ')
	assert out == expected

def test__help_formatter__line_break() -> None:
	raw = r'''
	usage: set key1=val1 [key2=val2 ...] \\
	       set key [=] val

	Change the value of a setting.
'''
	expected = '''\
usage: set key1=val1 [key2=val2 ...]
       set key [=] val

Change the value of a setting.'''

	out = HelpFormatter('prog')._fill_text(raw, width=80, indent='')
	assert out == expected

def test__help_formatter__list() -> None:
	raw = r'''
	features:
	- type safe. This is a rather long and complicated point that can no way fit on a single line.
	- useful error messages
	  - for syntax errors. There are so many different reasons for syntax errors that there is no way to explain them all on one line.
	  - for invalid keys
	  - for invalid values
	- create default config file
	  - with current settings
	  - with help
'''
	expected = '''\
features:
- type safe. This is a rather long and complicated
  point that can no way fit on a single line.
- useful error messages
  - for syntax errors. There are so many different
    reasons for syntax errors that there is no way
    to explain them all on one line.
  - for invalid keys
  - for invalid values
- create default config file
  - with current settings
  - with help'''

	out = HelpFormatter('prog')._fill_text(raw, width=50, indent='')
	assert out == expected

def test__format_text__text_list() -> None:
	raw = r'''
	This is an explanatory parapraph which is followed by a list:
	- a
	- b
	- but you should definitely not forget c either
'''
	expected = '''\
This is an explanatory
parapraph which is
followed by a list:
- a
- b
- but you should
  definitely not forget c
  either

'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out == expected

def test__format_text__list_merge_lines() -> None:
	raw = r'''
	- foo
	- bar
	  baz
'''
	expected = '''\
- foo
- bar baz'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out.rstrip() == expected

def test__format_text__list_with_line_break() -> None:
	raw = r'''
	- foo
	- bar \\
	  baz
'''
	expected = '''\
- foo
- bar
  baz'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out.rstrip() == expected

def test__format_text__text_list_text() -> None:
	raw = r'''
	This is an explanatory parapraph which is followed by a list.

	- a
	- b
	- but you should definitely not forget c either

	There may be another paragraph following.
'''
	expected = '''\
This is an explanatory
parapraph which is
followed by a list.

- a
- b
- but you should
  definitely not forget c
  either

There may be another
paragraph following.'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out.rstrip() == expected


def test__format_text__gitlab_task_list() -> None:
	raw = r'''
	- [x] Completed task
	- [~] Inapplicable task
	- [ ] Incomplete task
	  - [x] Sub-task 1 with a pretty long description
	  - [~] Sub-task 2
	  - [ ] Sub-task 3

	1. [x] Completed task
	1. [~] Inapplicable task that will not fit on one line
	1. [ ] Incomplete task
	   1. [x] Sub-task 1
	   1. [~] Sub-task 2
	   1. [ ] Sub-task 3
'''
	expected = '''\
- [x] Completed task
- [~] Inapplicable task
- [ ] Incomplete task
  - [x] Sub-task 1 with a
        pretty long
        description
  - [~] Sub-task 2
  - [ ] Sub-task 3

1. [x] Completed task
1. [~] Inapplicable task
       that will not fit
       on one line
1. [ ] Incomplete task
   1. [x] Sub-task 1
   1. [~] Sub-task 2
   1. [ ] Sub-task 3'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out.rstrip() == expected


def test__format_text__nbsp() -> None:
	raw = r'''
	source /a/super/long/path/which/would/cause/a/break
	source /a/super/long/path/which/would/cause/a/break'''
	expected = '''\
source
/a/super/long/path/which/would/cause/a/break
source /a/super/long/path/which/would/cause/a/break'''

	out = HelpFormatterWrapper(HelpFormatter, width=25).format_text(raw)
	assert out.rstrip() == expected

def test__split_lines__nbsp(capsys: 'pytest.CaptureFixture[str]') -> None:
	epilog = '''
	add the following to your ~/.bash_completion: `source /a/very/long/path/to/complete.sh`

	add the following to your ~/.bash_completion: `source /a/very/long/path/to/complete.sh`
	'''

	p = argparse.ArgumentParser(formatter_class=HelpFormatter, prog='test', epilog=epilog)
	p.add_argument('--normal-break', action='store_true', help="you can use a non-breaking space to prevent a line break but it will be printed as a normal space")
	p.add_argument('--testing-nbsp', action='store_true', help="you can use a non-breaking space to prevent a line break but it will be printed as a normal space")
	expected = f'''\
usage: test [-h] [--normal-break] [--testing-nbsp]

{'optional arguments' if sys.version_info < (3, 10) else 'options'}:
  -h, --help      show this help message and exit
  --normal-break  you can use a non-breaking space to prevent a line
                  break but it will be printed as a normal space
  --testing-nbsp  you can use a non-breaking space to prevent a
                  line break but it will be printed as a normal space

add the following to your ~/.bash_completion: `source
/a/very/long/path/to/complete.sh`

add the following to your ~/.bash_completion:
`source /a/very/long/path/to/complete.sh`
'''

	with pytest.raises(SystemExit):
		p.parse_args(['--help'])

	assert capsys.readouterr().out == expected


# ------- HelpFormatterWrapper add/format_help -------

def test__help_formatter__add_text() -> None:
	f = HelpFormatterWrapper(HelpFormatter)
	f.add_text('hello world')
	f.add_text('hello again')

	expected = '''\
hello world

hello again
'''

	assert f.format_help() == expected

def test__help_formatter__add_item_default_bullet() -> None:
	f = HelpFormatterWrapper(HelpFormatter, width=20)
	f.add_start_list()
	f.add_item('foo')
	f.add_item('bar')
	f.add_item('and a long item which requires breaking')
	f.add_end_list()

	expected = '''\
- foo
- bar
- and a long item
  which requires
  breaking
'''

	assert f.format_help() == expected

def test__help_formatter__add_item_nbsp() -> None:
	f = HelpFormatterWrapper(HelpFormatter, width=25)
	f.add_start_list()
	f.add_item('and a long item which would break')
	f.add_item('and a long item which would break')
	f.add_end_list()

	expected = '''\
- and a long item which
  would break
- and a long item
  which would break
'''

	assert f.format_help() == expected

def test__help_formatter__add_item_custom_bullet() -> None:
	f = HelpFormatterWrapper(HelpFormatter, width=25)
	pattern = '%s: '
	f.add_start_list()
	f.add_item(bullet=pattern % 42, text='The answer to everything')
	f.add_item(bullet=pattern % 23, text='The natural number following 22 and preceding 24')
	f.add_end_list()

	expected = '''\
42: The answer to
    everything
23: The natural number
    following 22 and
    preceding 24
'''

	assert f.format_help() == expected

def test__help_formatter__add_text_and_item() -> None:
	f = HelpFormatterWrapper(HelpFormatter, width=25)
	pattern = '%s: '
	f.add_text('This is about some numbers and the meaning of life.')
	f.add_start_list()
	f.add_item(bullet=pattern % 42, text='The answer to everything')
	f.add_item(bullet=pattern % 23, text='The natural number following 22 and preceding 24')
	f.add_end_list()
	f.add_text('''I hope you've got this.''')

	expected = '''\
This is about some
numbers and the meaning
of life.

42: The answer to
    everything
23: The natural number
    following 22 and
    preceding 24

I hope you've got this.
'''

	assert f.format_help() == expected


# ---------- argparse actions ----------
# CallAction is mostly tested indirectly in test_quickstart.py

def test_callaction__error_if_help_is_missing() -> None:
	p = argparse.ArgumentParser()

	def do_nothing() -> None:
		return

	with pytest.raises(TypeError, match="missing doc string for function do_nothing"):
		p.add_argument('--do-nothing', action=CallAction, callback=do_nothing)

def test_callaction__pass_help_instead_of_doc_string(capsys: 'pytest.CaptureFixture[str]') -> None:
	p = argparse.ArgumentParser()

	def do_nothing() -> None:
		'''private'''
		return

	p.add_argument('--do-nothing', action=CallAction, callback=do_nothing, help="do nothing")

	with pytest.raises(SystemExit):
		p.parse_args(['--help'])

	out = capsys.readouterr().out
	assert "private" not in out
	assert "do nothing" in out

def test_callaction__cleanup_docstring(capsys: 'pytest.CaptureFixture[str]') -> None:
	p = argparse.ArgumentParser(formatter_class=HelpFormatter)

	def do_nothing() -> None:
		'''
		This function does nothing.

		It is just a test that doc strings are cleaned correctly.
		'''
		return

	p.add_argument('--do-nothing', action=CallAction, callback=do_nothing)

	with pytest.raises(SystemExit):
		p.parse_args(['--help'])

	out = [ln.rstrip() for ln in capsys.readouterr().out.splitlines()]
	expected = '''\
  --do-nothing  This function does nothing.

                It is just a test that doc strings are cleaned
                correctly.
'''.splitlines()
	assert expected == out[-len(expected):]

def test_callaction__no_args(capsys: 'pytest.CaptureFixture[str]') -> None:
	p = argparse.ArgumentParser(formatter_class=HelpFormatter)

	def do_nothing() -> None:
		'''This function does nothing.'''
		return

	p.add_argument('--do-nothing', action=CallAction, callback=do_nothing, nargs=0)
	p.parse_args(['--do-nothing'])
	# CallAction.__call__ parameter values gets an empty list, not None

def test_callaction__exactly_one_arg(capsys: 'pytest.CaptureFixture[str]') -> None:
	p = argparse.ArgumentParser(formatter_class=HelpFormatter)

	def do_nothing(arg: str) -> None:
		'''This function does nothing.'''
		return

	p.add_argument('--do-nothing', action=CallAction, callback=do_nothing, nargs=1)
	p.parse_args(['--do-nothing', 'Why should I give an arg?'])
	# CallAction.__call__ parameter values gets a list with one element, not just the str

def test_callaction__values_none_and_str(capsys: 'pytest.CaptureFixture[str]') -> None:
	p = argparse.ArgumentParser(formatter_class=HelpFormatter)

	def do_nothing(arg: 'str|None' = None) -> None:
		'''This function does nothing.'''
		print('That was a lie. I am printing something.')
		return

	p.add_argument('--do-nothing', action=CallAction, callback=do_nothing, nargs='?')
	p.parse_args(['--do-nothing', 'Why should I give an arg?'])
	p.parse_args(['--do-nothing'])
