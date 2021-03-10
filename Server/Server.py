# -*- coding: utf-8 -*-

from select import select
import socket

# My modules
from modules import Requests


class Server(object):
	def __init__(self, host='localhost', port=8080):
		self.host = host
		self.port = port

		self.tasks = []
		self.to_read = {}
		self.to_write = {}

		self.post_requests = Requests.Requests()

		self.tasks.append(self.start())


	def start(self):
		print('The Server is running...')

		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((self.host, self.port))
		server_socket.listen()

		while True:
			yield ('read', server_socket)
			client_socket, addr = server_socket.accept()
			self.tasks.append(self.client(client_socket, addr))


	def client(self, sock, addr):
		while True:
			yield ('read', sock)

			try:
				data = sock.recv(4096)
			except (ConnectionResetError, ConnectionAbortedError):
				continue

			if not data:
				break

			else:
				requestFrom = eval(data.decode())
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
	try:
		server = Server()
		server.run()
	except KeyboardInterrupt:
		print('Server is close...')