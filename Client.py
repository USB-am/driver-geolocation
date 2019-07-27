# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM


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


class User(object):

	__slots__ = ('host', 'port')

	def __init__(self, host='localhost', port=8000):

		self.host = host
		self.port = port


	@check_server_error
	@check_server_response
	def enterApp(self, login, password):

		print('Авторизация пользователя "%s"' % login)
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((self.host, self.port))

		enterForm = ('check_log_in', (login, password))
		sock.send(str(enterForm).encode())
		answer = sock.recv(128)

		return (sock, answer)


	@check_server_error
	@check_server_response
	def registration(self, login, password, user_name, car='Неизвестно'):

		print('Регистрация пользователя "%s"' % login)
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((self.host, self.port))

		registrationForm = ('registration', (login, password, user_name, car))
		sock.send(str(registrationForm).encode())
		answer = sock.recv(128)

		return (sock, answer)


	@check_server_error
	def create_new_route(self, sock, driver, start_date, finish_date, start_point, finish_point):

		print('Создание нового маршрута от %s до %s' % (start_point, finish_point))
		createForm = ('create_new_route', (driver, start_date, finish_date, start_point, finish_point))
		sock.send(str(createForm).encode())
		data = sock.recv(128)
		answer = eval(data.decode())

		if isinstance(answer, tuple):
			return False
		return True


	@check_server_error
	def update_route(self, sock, col, old, new):

		print('Изменение маршрута')
		updateForm = ('update_route', (col, old, new))
		sock.send(str(updateForm).encode())
		data = sock.recv(128)
		answer = eval(data.decode())

		return answer


	@check_server_error
	def get_routes(self, sock, start=0, rows=20):

		while True:

			get_routesForm = ('get_routes', (start, rows))
			sock.send(str(get_routesForm).encode())
			data = sock.recv(64 * rows)
			answer = eval(data.decode())

			yield answer
			start += rows


	@check_server_error
	def new_coords(self, sock, row_route, coords):

		coordsForm = ('new_coords', (row_route, coords))
		sock.send(str(coordsForm).encode())
		data = sock.recv(4096)
		answer = eval(data.decode())

		return answer


	@check_server_error
	def delete_route(self, sock, driver, start_date, finish_date):

		deleteForm = ('delete_route', (driver, start_date, finish_date))
		sock.send(str(deleteForm).encode())
		data = sock.recv(4096)
		answer = eval(data.decode())

		return answer


if __name__ == '__main__':

	from random import randint
	import datetime

	routes = []

	u1 = User()
	x = u1.enterApp('123', '123')

	if not x:
		x = u1.registration('123', '123', 'Usbam')

	if x:
		c = u1.get_routes(x)

		# ========================= TEMP ============================
		name = ''.join([chr(randint(65, 91)) for x in range(7)])
		sd = datetime.datetime(2019, randint(1, 12), randint(1, 28))
		fd = datetime.datetime(2019, randint(1, 12), randint(1, 28))
		if sd > fd:
			sd, fd = fd, sd
		sd = sd.strftime('%d.%m.%Y')
		fd = fd.strftime('%d.%m.%Y')
		p = lambda: float('%s.%s' % (randint(0, 100), randint(10**10, 10**11)))

		# route = u1.create_new_route(x, name, sd, fd, str((p(), p())), str((p(), p())))

		newCoords = tuple([(p(), p()) for x in range(randint(2, 8))])

		ncs = u1.new_coords(x, 3, newCoords)

		# dr = u1.delete_route(x, 'Usbam', '15.07.2019', '16.07.2019')
		# print(dr)

		# while True:
		# 	coords = next(c)
		# 	if not any(coords):
		# 		break
		# 	routes.extend(coords)

		# u1.update_route(x, 'Driver', 'Ivan', 'Usbam')