#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbutil import MySQLConnection


class User(object):
	table = 'users'
	key = 'id'
	columns_select = ['id', 'username', 'password', 'email']
	columns_add = ['username', 'password', 'email']
	columns_update = ['email']

	@classmethod
	def validate_login(cls, username, password):
		_columns = ('id', 'username')
		_sql = 'select id, username from users where username=%s and password=md5(%s)'
		_count, _rt_list = MySQLConnection.execute_sql(_sql, (username, password))
		return dict(zip(_columns, _rt_list[0])) if _count != 0 else None