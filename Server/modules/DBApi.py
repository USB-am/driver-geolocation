# -*- coding: utf-8 -*-

from collections.abc import Iterable
import sqlite3 as SQL
import os


class DataBase(object):
	def __init__(self, absolute_path, titles):
		# If folder not exist - create folder
		if not os.path.exists(os.path.dirname(absolute_path)):
			os.makedirs(os.path.dirname(absolute_path))

		# DataBase name
		self.name = os.path.basename(absolute_path)

		# Connect to DataBase
		self.connected = SQL.connect(absolute_path)
		# Create cursor for execute requests
		self.cursor = self.connected.cursor()

		# Create DataBase (if not exists)
		self.cursor.execute('''
			CREATE TALBE IF NOT EXISTS {name}
			{titles}
			PRIMARY KEY({id}))
			'''.format(
				name=self.name,
				titles=titles,
				id=titles[0].split(' ')[0]
			)
		)


	# Select columns from DataBase
	def select(self):
		# TODO: Return DB columns
		pass


	# Write new data in DataBase
	def write(self, titles):
		row_num = self.last_num_row + 1
		titles = (row_num, *titles)
		self.cursor.execute("""
			INSERT INTO {name}
			VALUES {titles}
			""".format(
				name=self.name,
				titles=titles
			)
		)
		self.connected.commit()	# Save changes


	# Last Id-number
	def last_num_row(self):
		self.cursor.execute("""
			SELECT COUNT(*) FROM {name}
			""".format(self.name)
		)
		answer = self.cursor.fetchall()
		return answer[0][0]