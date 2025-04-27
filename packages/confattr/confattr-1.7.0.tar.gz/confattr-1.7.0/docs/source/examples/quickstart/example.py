#!../../../../venv/bin/python3
# ------- start -------
'''
Print a greeting.
'''

APP_NAME = 'test-app'
__version__ = '1.0.0'

from confattr import Config, Message
from confattr.quickstart import ConfigManager

class App:

	greeting = Config('greeting', "hello world", help=
		"This setting is defined in the example and "
		"is not a standard setting defined by quickstart.")

	def __init__(self, config_manager: ConfigManager) -> None:
		self.cfg = config_manager
		self.ui_notifier = self.cfg.ui_notifier
		self.cfg.load()

	def main(self, greeting: 'str|None' = None) -> None:
		if greeting is None:
			greeting = self.greeting

		self.init_ui()
		self.cfg.set_ui_callback(self.show_message)
		self.mainloop(greeting)

	def init_ui(self) -> None:
		pass

	def mainloop(self, greeting: str) -> None:
		self.ui_notifier.show_info(greeting)
	
	def show_message(self, msg: Message) -> None:
		print(msg)

def main(largs: 'list[str]|None' = None) -> None:
	cfg = ConfigManager(APP_NAME, __version__, __doc__)
	p = cfg.create_argument_parser()
	p.add_argument('greeting', nargs='?', help="how you want to be greeted")

	args = p.parse_args(largs)
	app = App(cfg)
	app.main(args.greeting)

if __name__ == '__main__':
	main()
