# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from select import select

# === My modules ===
from Request import *


class Server(object):

	__slots__ = ('host', 'port', 'tasks', 'to_read', 'to_write', 'post_requests')

	def __init__(self, host='localhost', port=8000):

		self.host = host
		self.port = port

		self.tasks = []
		self.to_read = {}
		self.to_write = {}

		self.post_requests = Request()

		self.tasks.append(self.start())


	def start(self):

		print('The server is running...\n')

		server_socket = socket(AF_INET, SOCK_STREAM)
		server_socket.bind((self.host, self.port))
		server_socket.listen()

		while True:

			yield ('read', server_socket)
			client_socket, addr = server_socket.accept()
			self.tasks.append(self.client(client_socket, addr))


	def client(self, sock, *args):

		while True:

			yield ('read', sock)
			try:
				request = sock.recv(4096)

			except (ConnectionResetError, ConnectionAbortedError):
				continue

			if not request:
				break

			else:
				requestFrom = eval(request.decode())
				print(requestFrom)
				answer = self.post_requests(requestFrom)

				yield ('write', sock)
				sock.send(str(answer).encode())

		sock.close()


	def run(self):

		while any([self.tasks, self.to_read, self.to_write]):

			while not self.tasks:

				ready_to_read, ready_to_write, _ = select(self.to_read, self.to_write, [])

				for sock in ready_to_read:
					self.tasks.append(self.to_read.pop(sock))
				for sock in ready_to_write:
					self.tasks.append(self.to_write.pop(sock))

			try:
				task = self.tasks.pop(0)
				reason, sock = next(task)

				if reason == 'read':
					self.to_read[sock] = task

				if reason == 'write':
					self.to_write[sock] = task

			except StopIteration:
				pass


if __name__ == '__main__':
	global user_num

	user_num = 1

	server = Server()
	try:
		server.run()
	except KeyboardInterrupt:
		print('\nShut down server...')
		exit()