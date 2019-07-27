# -*- coding: utf-8 -*-

import os, sys
import time

# My modules
from DBApi import *


class Request(object):

	def __init__(self):

		self.Users = DataBase('Users')
		self.Users.newBase(titles=(
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

		self.Routes = DataBase('Routes')
		self.Routes.newBase(titles=(
				'Id int',
				'Driver varchar(100)',
				'Start_date varchar(10)',
				'Finish_date varchar(10)',
				'Start_point varchar(50)',
				'Finish_point varchar(50)',
				'Geolocation text'
			)
		)


	def __call__(self, form, *args, **kwargs):

		try:
			return eval('self.%s%s' % (form[0], form[1]))

		except AttributeError as e:
			print('Error AttributeError: self.%s%s\n\n%s' % (form[0], form[1], e))
			return False


	def check_log_in(self, login, password):

		answer = self.Users.select(
			"""
			SELECT * FROM %(name)s
			WHERE Email = '%(login)s' AND Password = '%(password)s'
			""" % {
				'name' : self.Users.file_name,
				'login' : login,
				'password' : password
			}
		)

		if answer == []:
			return False
		return True


	def registration(self, login, password, user_name, car=None):

		if not self.check_log_in(login, password):
			# print(self.Users.last_num_row())
			self.Users.write(request=
				"""
				INSERT INTO %(name)s
				VALUES %(titles)s
				""" % {
					'name' : self.Users.file_name,
					'titles' : (
						self.Users.last_num_row()+1,	# Id
						user_name,						# Name
						login,							# Login
						password,						# Password
						car,							# Car
						'Неизвестно',					# Currest_Route
						1,								# Status
						time.time()						# Enter_time
					)
				}
			)
			return True
		return False


	def create_new_route(self, driver, start_date, finish_date, start_point, finish_point):

		self.Routes.write(request=
			"""
			INSERT INTO %(name)s
			VALUES %(titles)s
			""" %  {
				'name' : self.Routes.file_name,
				'titles' : (
					self.Routes.last_num_row()+1,	# Id
					driver,
					start_date,
					finish_date,
					start_point,
					finish_point,
					'[]'
				)
			}
		)

		self.Users.write(request=
			"""
			UPDATE %(name)s SET Currest_Route = '%(route)s'
			WHERE Name = '%(driver)s'
			""" % {
				'name' : self.Users.file_name,
				'route' : 'From %s to %s' % (start_point, finish_point),
				'driver' : driver
			}
		)

		print('Done')
		return True


	# ====================== #
	# =    REWRITE IT'S    = #
	# ====================== #
	def update_route(self, column, old_column, new_column):

		self.Routes.write(request=
			"""
			UPDATE %(name)s SET %(col)s = '%(newCol)s'
			WHERE %(col)s = '%(oldCol)s'
			""" % {
				'name' : self.Routes.file_name,
				'col' : column,
				'oldCol' : old_column,
				'newCol' : new_column
			}
		)

		print('Done')
		return True


	def new_coords(self, route_id, crds):

		geolocations = self.Routes.select(request=
			"""
			SELECT Geolocation FROM %(name)s
			WHERE Id = '%(route_id)s'
			""" % {
				'name' : self.Routes.file_name,
				'route_id' : route_id
			}
		)

		try:
			geolocations = list(eval(geolocations[0][0]))
		except IndexError:
			return False

		if geolocations == None:
			geolocations = list(crds)
		else:
			geolocations.extend(list(crds))

		self.Routes.write(request=
			"""
			UPDATE %(name)s SET Geolocation = '%(update_list)s'
			WHERE Id = '%(route_id)s'
			""" % {
				'name' : self.Routes.file_name,
				'update_list' : str(geolocations),
				'route_id' : route_id
			}
		)

		print('Done')
		return True


	def delete_route(self, driver, start_date, finish_date):

		self.Routes.write(request=
			"""
			DELETE FROM %(name)s
			WHERE Driver = '%(driver)s' AND
			Start_date = '%(start_date)s' AND
			Finish_date = '%(finish_date)s'
			""" % {
				'name' : self.Routes.file_name,
				'driver' : driver,
				'start_date' : start_date,
				'finish_date' : finish_date
			}
		)

		print('Done')
		return True


	def get_routes(self, start, rows):

		routes = self.Routes.select(request=
			"""
			SELECT Driver, Start_date, Finish_date, Start_point, Finish_point
			FROM %(name)s LIMIT %(start)s, %(finish)s
			""" % {
				'name' : self.Routes.file_name,
				'start' : start,
				'finish' : start + rows
			}
		)

		return routes