# -*- coding: utf-8 -*-

import socket


def check_server_error(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except (ConnectionRefusedError, ConnectionResetError, AttributeError):
			print('Connection Error')
			return False
	return wrapper


def check_server_response(func):
	def wrapper(*args, **kwargs):
		sock, answer = func(*args, **kwargs)
		try:
			if eval(answer.decode()):
				return sock
			else:
				sock.close()
				return False
		except SyntaxError:
			print('AnswerError: task new data "%s"' % answer.decode())
			return False
	return wrapper


class Client(object):
	def __init__(self, host='localhost', port=8080):

		self.host = host
		self.port = port


	@check_server_error
	def connect(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.host, self.port))

		test_form = ('test', tuple([i for i in range(10)]))
		print(test_form)
		sock.send(str(test_form).encode())
		if eval(sock.recv(4096).decode()):
			return sock
		return


if __name__ == '__main__':
	client = Client()
	print(client.connect())