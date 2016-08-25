#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbutil import MySQLConnection
from encrypt import md5_str
import csv


class Assets_vms(object):
	@classmethod
	def get_host_list(cls):
		_columns = ('id','pip')
		_sql = 'select pid,pip from physics_host where status=0'
		args = ()
		result=[]
		_count,_rt_list = MySQLConnection.execute_sql(_sql,args)
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))
		else:
			result = []
		return result

	@classmethod
	def get_vmList(cls):
		_column='vid,vmid,application,vmip,os,cpuThread,mem,disk,bHost'
		_columns = _column.split(',')
		_sql = 'select {columns} from vms where status=0'.format(columns=_column)
		args = ()
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		result = []
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))

		return result

	@classmethod
	def get_vm_list(cls):
		_column = 'vid,vmid,application,vmip,os,cpuThread,mem,disk,bHost'
		_sql = 'select vms.vid,vms.vmid,vms.application,vms.vmip,oses.osname as os,vms.cpuThread,vms.mem,vms.disk,physics_host.pip as bHost from vms inner join physics_host on vms.bHost=physics_host.pid inner join oses on vms.os=oses.id  where physics_host.status=0'
		args = ()
		result = []
		_columns = _column.split(',')
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args)
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))
		else:
			result = []
		return result

	@classmethod
	def get_by_vmid(cls,key,value):
		_column = 'vid,vmid,application,vmip,os,cpuThread,mem,disk,bHost'
		_sql = 'select {column} from vms where status=0 and {k}=%s'.format(column=_column,k=key)
		args = (value,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		return dict(zip(_column.split(','), _rt_list[0])) if _count != 0 else None

	@classmethod
	def validate_vms_add(cls,vmid,vmip,os,cpuThread,mem,disk,bHost):
		error = []
		rt = True
		_rt_list = cls.get_by_vmid('vmid',vmid)
		if _rt_list:
			rt = False
			error.append('vmid已存在')
		if not vmid:
			rt = False
			error.append('vmid不能为空')
		vmip = vmip.strip()
		if vmip:
			ip = vmip.split('.')
			for a in ip:
				if not 0 <= int(a) <= 255:
					rt = False
					error.append('IP地址不正确')
					break
		elif len(vmip.split('.')) != 4:
			rt = False
			error.append('IP地址不正确')
		if cls.get_by_vmid('vmip',vmip):
			rt = False
			error.append('IP地址已存在')
			
		if not os or not cpuThread or not mem or not disk or not bHost:
			rt = False
			error.append('os/cpu核数/内存/硬盘/物理主机不能为空')
		if not os.isdigit() or not cpuThread.isdigit() or not mem.isdigit() or not disk.isdigit() or not bHost.isdigit():
			rt = False
			error.append('os/cpu核数/内存/硬盘/物理主机不是整数')
		return rt, error

	@classmethod
	def validate_vms_update(cls,vmid,vmip,os,cpuThread,mem,disk,bHost):
		error = []
		rt = True
		vmip = vmip.strip()
		if vmip:
			ip = vmip.split('.')
			for a in ip:
				if not 0 <= int(a) <= 255:
					rt = False
					error.append('IP地址不正确')
					break
		elif len(vmip.split('.')) != 4:
			rt = False
			error.append('IP地址不正确')
		if cls.get_by_vmid('vmip',vmip) != None and cls.get_by_vmid('vmip',vmip)['vmid'] != vmid:
			rt = False
			print rt
			error.append('IP地址已存在')			
		if not os or not cpuThread or not mem or not disk or not bHost:
			rt = False
			error.append('os/cpu核数/内存/硬盘/物理主机不能为空')
		if not os.isdigit() or not cpuThread.isdigit() or not mem.isdigit() or not disk.isdigit() or not bHost.isdigit():
			rt = False
			error.append('os/cpu核数/内存/硬盘/物理主机不是整数')
		return rt, error


	@classmethod
	def assets_vm_add(cls,vmid,application,vmip,os,cpuThread,mem,disk,bHost):
		_sql = 'insert into vms(vmid,application,vmip,os,cpuThread,mem,disk,bHost) values(%s,%s,%s,%s,%s,%s,%s,%s)'
		args = (vmid,application,vmip,os,cpuThread,mem,disk,bHost)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''


	@classmethod
	def assets_vm_update(cls,vmid,application,vmip,os,cpuThread,mem,disk,bHost):
		_sql = 'update vms set vmip=%s,application=%s,os=%s,cpuThread=%s,mem=%s,disk=%s,bHost=%s where vmid=%s and status=0'
		args = (vmip,application,os,cpuThread,mem,disk,bHost,vmid)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args, False)
		if _count:
			return True, ''
		else:
			return False, ''

	@classmethod
	def assets_vm_delete(cls,vmid):
		_sql = 'update vms set status=1 where vmid=%s'
		args = (vmid,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		if _count:
			return True, ''
		else:
			return False, ''

			
class Assets_physics(object):
	@classmethod
	def get_os_list(cls):
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
	def get_idcs_list(cls):
		_column = 'id,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address'
		_columns = _column.split(',')
		_sql = 'select {columns} from idcs where status=0'.format(columns=_column)
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
	def get_by_key(cls,k=1,v=1):
		_column='pid,sn,pip,vendor,model,esxi_version,cpuModel,pmem,PurchaseDate,warranty,bIdc,bPod,bPu'
		_columns = _column.split(',')
		_sql = 'select {columns} from physics_host where status=0 and {k} = %s'.format(columns=_column,k=k)
		args = (v,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		return dict(zip(_columns, _rt_list[0])) if _count != 0 else None

	@classmethod
	def get_hostList(cls):
		_column='pid,sn,pip,vendor,model,esxi_version,cpuModel,pmem,PurchaseDate,warranty,bIdc,bPod,bPu'
		_columns = _column.split(',')
		_sql = 'select {columns} from physics_host where status=0'.format(columns=_column)
		args = ()
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		result = []
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))

		return result
	
	@classmethod
	def get_host_address(cls,bIdc,bPod,bPu):
		_column='pid,sn,pip,vendor,model,esxi_version,cpuModel,pmem,PurchaseDate,warranty,bIdc,bPod,bPu'
		_columns = _column.split(',')
		_sql = 'select {columns} from physics_host where status=0 and bIdc= %s and bPod=%s and bPu=%s'.format(columns=_column)
		args=(bIdc,bPod,bPu)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args)
		return dict(zip(_columns, _rt_list[0])) if _count != 0 else None


	@classmethod
	def get_assets_physics(cls):
		_sql = 'select physics_host.pid,physics_host.sn,physics_host.pip,physics_host.vendor,physics_host.model,oses.osname as esxi_version,physics_host.cpuModel,physics_host.pmem,physics_host.PurchaseDate,physics_host.warranty,physics_host.bPod,physics_host.bPu, idcs.idcName as bIdc from physics_host inner join oses on physics_host.esxi_version=oses.id inner join idcs on physics_host.bIdc=idcs.id where physics_host.status=0'
		_columns = ('pid','sn','pip','vendor','model','esxi_version','cpuModel','pmem','PurchaseDate','warranty','bPod','bPu','bIdc')
		args = ()
		_count,_rt_list = MySQLConnection.execute_sql(_sql, args)
		result = []
		if _count:
			for rt in _rt_list:
				result.append(dict(zip(_columns, rt)))
		else:
			result = []
		return result

	@classmethod
	def validate_physics_create(cls,sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu):
		_rt_list = cls.get_by_key('sn',sn)
		error = []
		rt = True
		if _rt_list:
			rt = False
			error.append('sn号已存在')
		if len(sn) != 10:
			rt = False
			error.append('sn号长度不正确')
		pip = pip.strip()
		if pip:
			ip = pip.split('.')
			for a in ip:
				if not 0 <= int(a) <= 255:
					rt = False
					error.append('IP地址不正确')
					break
		elif len(pip.split('.')) != 4:
			rt = False
			error.append('IP地址不正确')
		elif cls.get_by_key('pip',pip):
			rt = False
			error.append('IP地址已存在')
		if not vendor or not model or not esxi_version or not purchase_date or not warranty or not bIdc or not bPod or not bPu:
			rt = False
			error.append('厂商/型号/系统版本/采购日期/保修年限/IDC/机柜/机柜位置不能为空')
		if not esxi_version.isdigit() or not warranty.isdigit() or not bIdc.isdigit() or not pmem.isdigit():
			rt = False
			error.append('保修年限/机房ID/内存不是整数')
		_ipu = cls.get_host_address(bIdc,bPod,bPu)
		if _ipu:
			rt = False
			error.append('该机房所选机柜位置已存在服务器')
		return rt, error

	@classmethod
	def assets_physics_add(cls,sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu):
		#_columns=('sn','pip','vendor','model','esxi_version','cpuModel', 'pmem','PurchaseDate', 'warranty','bIdc', 'bPod', 'bPu')
		_sql = 'insert into physics_host(sn, pip, vendor, model, esxi_version, cpuModel, pmem, PurchaseDate, warranty, bIdc, bPod, bPu) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		args = (sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu)
		_count, _rt_list = MySQLConnection.execute_sql(_sql, args,False)
		if _count:
			return True, ''
		else:
			return False, ''
		

	@classmethod
	def validate_physics_update(cls,sn,pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu):
		error = []
		rt = True
		if pip:
			ip = pip.strip().split('.')
			for a in ip:
				if not 0 <= int(a) <= 255:
					rt = False
					error.append('IP地址不正确')
					break
		elif len(pip.strip().split('.')) != 4:
			rt = False
			error.append('IP地址不正确')
		else:
			rt = False
			error.append('IP地址不能为空')
		if not vendor or not model or not esxi_version or not purchase_date or not warranty or not bIdc or not bPod or not bPu:
			rt = False
			error.append('厂商/型号/系统版本/采购日期/保修年限/IDC/机柜/机柜位置不能为空')
		if not esxi_version.isdigit() or not warranty.isdigit() or not bIdc.isdigit() or not pmem.isdigit():
			rt = False
			error.append('保修年限/机房ID/内存不是整数')
		_ipu = cls.get_host_address(bIdc,bPod,bPu)
		if _ipu['sn'] != sn:
			rt = False
			error.append('该机房所选机柜位置已存在服务器')
		return rt, error

	@classmethod
	def assets_physics_update(cls,sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu):
		_sql = 'update physics_host set pip=%s, vendor=%s,model=%s,esxi_version=%s,cpuModel=%s, pmem=%s, PurchaseDate=%s,warranty=%s,bIdc=%s,bPod=%s,bPu=%s where sn=%s'
		args = (pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu, sn)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''

	@classmethod
	def assets_physics_delete(cls,sn):
		_sql = 'update physics_host set status=1 where sn=%s'
		args = (sn,)
		_count, _rt_list = MySQLConnection.execute_sql(_sql,args,False)
		if _count:
			return True, ''
		else:
			return False, ''

class Assets_import(object):
	@classmethod
	def import_vms(cls,csvFile):
		csvFile = file(csvFile,'rb')
		reader = csv.reader(csvFile)
		rowlists = []
		for line in reader:
			rowlists.append(line)
		csvFile.close()

		_columns = ','.join(rowlists[0][:-1])
		_datelists = rowlists[1:-1]
		_sql = 'insert into vms({columns}) values(%s,%s,%s,%s,%s,%s)'.format(columns=_columns)
		_count, _rt_list = MySQLConnection.bulker_execute_sql_vms(_sql,_datelists)
		if _count:
			return True, ''
		else:
			return False, ''

	@classmethod
	def import_physics(cls,csvFile):
		csvFile = file(csvFile,'rb')
		reader = csv.reader(csvFile)
		rowlists = []
		for line in reader:
			print line
			rowlists.append(line)
		csvFile.close()

		_columns = ','.join(rowlists[0])
		_datelists = rowlists[1:]
		_sql = 'insert into physics_host({columns}) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(columns=_columns)
		_count, _rt_list = MySQLConnection.bulker_execute_sql_physics(_sql,_datelists)
		if _count:
			return True, ''
		else:
			return False, ''
