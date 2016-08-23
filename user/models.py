#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbutil import MySQLConnection
from encry import md5_str

class UserType(object):
	@classmethod
	def get_user_types(cls):
		_sql = 'select tid, tname from user_types'
		_count, _rt_list = MySQLConnection.execute_sql(_sql,())
		return _rt_list



class User(object):
	table = 'users'
	key = 'id'
	columns_select = ['uid', 'username', 'password', 'email']
	columns_add = ['username', 'password', 'email']
	columns_update = ['email']

	@classmethod
	def validate_login(cls, username, password):
		_columns = ('uid', 'username', 'user_type')
		_sql = 'select uid, username, user_type from users where username=%s and password=md5(%s)'
		_count, _rt_list = MySQLConnection.execute_sql(_sql, (username, password))
		return dict(zip(_columns, _rt_list[0])) if _count != 0 else None

	@classmethod
	def get_users(cls):
		#_sql = 'select * from users where status=0'
		_sql = 'select users.uid, users.username,users.password, users.email, user_types.tname as user_type  from users inner join user_types on users.user_type = user_types.tid where status=0;'
		_columns = ('uid', 'username', 'password', 'email', 'user_type')
		_count, _rt_list = MySQLConnection.execute_sql(_sql,())
		userlist = []
		for i in _rt_list:
			userlist.append(dict(zip(_columns, i)))
		return userlist


	@classmethod
	def get_user_by(cls,k,v):
		_sql = 'select * from users where status=0 and {k}=%s'.format(k=k)
		args=(v,)
		_columns = ('uid', 'username', 'password', 'email', 'user_type')
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		return dict(zip(_columns, _rt_list[0])) if _count != 0 else None


	@classmethod
	def validate_user_add(cls,username, password, reppassword):
		errors = []
		if len(username) < 6:
			errors.append('用户名长度不能小于6')
		if password != reppassword:
			errors.append('两次密码输入不一致')
		if len(password) <8:
		 	errors.append('密码长度不能小于8')
		_rt_list = cls.get_user_by('username', username)
		if _rt_list:
			errors.append('用户名已存在')
		if errors:
			return False, '\n'.join(errors)
		else:
			return True, '' 

	@classmethod
	def user_add(cls, username,password, email, user_type):
		_sql = 'insert into users(username,password,email,user_type) values(%s, md5(%s),%s,%s)'
		_count, _rt_list = MySQLConnection.execute_sql(_sql,(username,password, email, user_type), False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod
	def user_update(cls, uid, username, email, user_type):
		_sql = 'update users set email=%s, user_type=%s where uid=%s and username=%s'
		args = (email, user_type, uid, username)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args, False)
		if _count:
			return True, ''
		else:
			return False, ''

	@classmethod
	def user_delete(cls, uid,username):
		_sql = 'delete from users where uid=%s and username=%s'
		args = (uid,username)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args, False)

		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod
	def up_password(cls,uid,username, newpassword):
		_sql = 'update users set password=md5(%s) where uid=%s and username=%s'
		args = (newpassword, uid, username)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args, False)
		if _count:
			return True, ''
		else:
			return False
		
