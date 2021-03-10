# -*- coding: utf-8 -*-

import datetime
from colorama import init, Fore, Style
import os
# My modules
from . import DBApi as DB


init()

now_date = datetime.datetime.now()
_path_to_log_file = ''.join(
	[
		os.path.split(os.path.dirname(__file__))[0],
		'\\logs\\%s-%s.txt' % (now_date.month, now_date.year)
	])
print(_path_to_log_file)

if os.path.exists(os.path.dirname(_path_to_log_file)):
	LOG_FILE = open(_path_to_log_file, mode='a', encoding='utf-8')
else:
	os.makedirs(os.path.dirname(_path_to_log_file))
	LOG_FILE = open(_path_to_log_file, mode='w', encoding='utf-8')


def logger(func):
	def wrapper(slf, requestForm, *args, **kwargs):
		answer = func(slf, requestForm=('test', (0, 1)))
		if answer:	color = Fore.GREEN
		else:	color = Fore.RED
		log_text = '{color}[{date}] {func_name}{func_args}: {status}{end}'.format(
			color = color,
			date = datetime.datetime.now(),
			func_name = requestForm[0],
			func_args = requestForm[1],
			status = answer,
			end = Style.RESET_ALL
		)
		print(log_text)
		LOG_FILE.write(log_text)
		return answer
	return wrapper


class Requests(object):
	def __init__(self):
		pass


	@logger
	def __call__(self, requestForm, *args, **kwargs):
		try:
			return eval('self.%s%s' % (requestForm[0], requestForm[1:]))
		except Exception as e:
			print(e)
			return False


	def test(self, *args, **kwargs):
		return True