# -*- coding: utf-8 -*-

import sqlite3 as SQL
import os, sys


class DataBase(object):

	def __init__(self, file_name):

		self.file_name = file_name
		self.path = os.path.dirname(__file__)
		os.system('md %s\\db' % self.path)

		self.conn = SQL.connect('%s\\db\\%s.db' % (self.path, self.file_name))
		self.cursor = self.conn.cursor()


	def newBase(self, titles):

		self.cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS %(name)s
			%(titles)s,
			PRIMARY KEY(%(id)s))
			""" % {
				'name' : self.file_name,
				'titles' : str(tuple(titles))[:-1].replace("'", ""),
				'id' : str(titles[0]).split(' ')[0]
			}
		)

		self.conn.commit()


	def select(self, request):

		self.cursor.execute(request)
		answer = self.cursor.fetchall()
		self.conn.commit()

		return answer


	def write(self, request):

		self.cursor.execute(request)
		self.conn.commit()


	def last_num_row(self):

		last_num = self.select(
			"""
			SELECT COUNT(*) FROM %s
			""" % self.file_name
		)

		return last_num[0][0]


if __name__ == '__main__':
	db = DataBase('Users')
	db.newBase(titles=(
			'Id int',
			'Name varchar(100)',
			'Email varchar(50)',
			'Password varchar(100)',
			'Car varchar(50)',
			'Currest_Route varchar(100)',
			'Status int',
			'Enter_Time float'
		)
	)
	print('Done')