#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbutil import MySQLConnection

class Idcs(object):
	@classmethod
	def get_idc_list(cls):
		_colunm = 'id,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address'
		_sql = 'select {column} from idcs where status=0'.format(column=_colunm)
		args = ()
		rt = []
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args)
		if _count:
			for idc in _rt_list:
				rt.append(dict(zip(_colunm.split(','), idc)))
		return rt


	@classmethod
	def get_by_id(cls,key,value):
		_colunm = 'id,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address'
		_sql = 'select {column} from idcs where status=0 and {key}=%s'.format(column=_colunm,key=key)
		args = (value,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args)
		return dict(zip(_colunm.split(','),_rt_list[0])) if _count !=0 else None


	@classmethod
	def validate_idc_add(cls,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,address):
		error = []
		if not idcName.strip():
			error.append('机房名称不能为空')
		if cls.get_by_id('idcName',idcName):
			error.append('机房名称已存在')
		if not pods.strip():
			error.append('机柜编号不能为空')
		if not bandwidth.strip() or not bandwidth.isdigit():
			error.append['带宽不能为空或不为整数']
		if not t_contact.strip() or not t_phone.strip() or not kf_contact.strip() or not kf_phone.strip():
			error.append('联系人或电话不能为空')
		if not address.strip():
			error.append('机房地址不能为空')
		if error:
			return False, error
		else:
			return True, ''

	
	@classmethod
	def validate_idc_update(cls,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,address):
		error = []
		if not pods.strip():
			error.append('机柜编号不能为空')
		if not bandwidth.strip() or not bandwidth.isdigit():
			error.append['带宽不能为空或不为整数']
		if not t_contact.strip() or not t_phone.strip() or not kf_contact.strip() or not kf_phone.strip():
			error.append('联系人或电话不能为空')
		if not address.strip():
			error.append('机房地址不能为空')
		if error:
			return False, error
		else:
			return True, ''



	@classmethod	
	def idc_add(cls,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address):
		_sql = 'insert into idcs(idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		args = (idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod	
	def idc_update(cls,_id,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address):
		_sql = 'update idcs set pods=%s,bandwidth=%s,t_contact=%s,t_phone=%s,kf_contact=%s,kf_phone=%s,start_date=%s,address=%s where id=%s and idcName=%s'
		args = (pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address,_id,idcName)
		_count, error = MySQLConnection.execute_sql(_sql, args, False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod	
	def idc_delete(cls,_id):
		_sql = 'update idcs set status=1 where id=%s'
		args = (_id,)
		_count, error = MySQLConnection.execute_sql(_sql, args, False)
		if _count:
			return True, ''
		else:
			return False, ''


class UserType(object):
	@classmethod
	def get_usertype_list(cls):
		_columns=('tid','tname')
		_sql = 'select tid,tname from user_types'
		args = ()
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		result = []
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))
		else:
			result = []
		return result


	@classmethod
	def get_usertype_by(cls,key,value):
		_column=('tid','tname')
		_sql = 'select tid,tname from user_types where {key}=%s'.format(key=key)
		args = (value,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args)
		return dict(zip(_column,_rt_list[0])) if _count !=0 else None

	@classmethod
	def validate_usertype_add(cls,tname):
		if not tname.strip():
			return False,'系统名称不能为空'
		else:
			_rt_tname = cls.get_usertype_by('tname',tname)
			if _rt_tname:
				return False,'用户类型已存在'
			else:
				return True,''


	@classmethod	
	def usertype_add(cls,tname):
		_sql = 'insert into user_types(tname)values(%s)'
		args = (tname,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod	
	def usertype_delete(cls,_tid):
		_sql = 'delete from user_types where tid=%s'
		args = (_tid,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''


class Oses(object):
	@classmethod
	def get_oses_list(cls):
		_columns=('id','osname')
		_sql = 'select id,osname from oses where status=0'
		args = ()
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		result = []
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))
		else:
			result = []
		return result


	@classmethod
	def get_os_by(cls,key,value):
		_column=('id','osname')
		_sql = 'select id,osname from oses where status=0 and {key}=%s'.format(key=key)
		args = (value,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args)
		return dict(zip(_column,_rt_list[0])) if _count !=0 else None

	@classmethod
	def validate_os_add(cls,osname):
		if not osname.strip():
			return False,'系统名称不能为空'
		else:
			_rt_os = cls.get_os_by('osname',osname)
			if _rt_os:
				return False,'操作系统已存在'
			else:
				return True,''


	@classmethod	
	def oses_add(cls,osname):
		_sql = 'insert into oses(osname)values(%s)'
		args = (osname,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod	
	def oses_delete(cls,_id):
		_sql = 'update oses set status=1 where id=%s'
		args = (_id,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''





