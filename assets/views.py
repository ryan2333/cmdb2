#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assets import assets
from flask import render_template, request, flash, redirect
from model import Assets_physics, Assets_vms, Assets_import
import json,time,csv
from StringIO import StringIO


def get_idcs():
	_idcs = Assets_physics.get_idcs_list()
	rt = []
	for _idc in _idcs:
		rt.append((_idc['id'],_idc['idcName']))
	return rt


@assets.route('/assets_vm/')
def assets_vm_list():
	assets_vm = Assets_vms.get_vm_list()
	return render_template('assets_vm.html', assets=assets_vm)


@assets.route('/assets_vm/create/')
def assets_vm_create():
	_oses = Assets_physics.get_os_list()
	_physics_hosts = Assets_vms.get_host_list()
	return render_template('assets_vm_create.html', oses=_oses, physics_hosts=_physics_hosts)


@assets.route('/assets_vm/add/',methods=['post'])
def assets_vm_add():
	params = request.form
	vmid = params.get('vmid','')
	application = params.get('application','') 
	vmip = params.get('vmip','') 
	os = params.get('os','')
	cpuThread = params.get('cpuThread',4)
	mem = params.get('mem',4)
	disk = params.get('disk',100)
	bHost = params.get('bHost','')
	_is_ok, error = Assets_vms.validate_vms_add(vmid,vmip,os,cpuThread,mem,disk,bHost)
	if _is_ok:
		is_ok,error = Assets_vms.assets_vm_add(vmid,application,vmip,os,cpuThread,mem,disk,bHost)
		return json.dumps({'is_ok':is_ok, 'success':'虚拟机添加成功'})
	else:
		return json.dumps({'is_ok':is_ok, 'error':'\n'.join(error)})


@assets.route('/assets_vm/modify/')
def assets_vm_modify():
	vid = request.args.get('vid')
	_oses = Assets_physics.get_os_list()
	_physics_hosts = Assets_vms.get_host_list()
	_assets = Assets_vms.get_by_vmid('vid', vid)
	return render_template('assets_vm_modify.html', oses=_oses, physics_hosts=_physics_hosts, assets=_assets)


@assets.route('/assets_vm/update/',methods=['post'])
def assets_vm_update():
	params = request.form
	vid = params.get('vid','')
	vmid = params.get('vmid','')
	application = params.get('application','') 
	vmip = params.get('vmip','') 
	os = params.get('os','')
	cpuThread = params.get('cpuThread',4)
	mem = params.get('mem',4)
	disk = params.get('disk',100)
	bHost = params.get('bHost','')
	_is_ok, error = Assets_vms.validate_vms_update(vmid,vmip,os,cpuThread,mem,disk,bHost,vid)
	if _is_ok:
		_is_ok,error = Assets_vms.assets_vm_update(vmid,application,vmip,os,cpuThread,mem,disk,bHost,vid)
		return json.dumps({'is_ok':_is_ok, 'success':'虚拟机信息更新成功'})
	else:
		return json.dumps({'is_ok':_is_ok, 'error':'\n'.join(error)})
	return ''


@assets.route('/assets_vm/delete/')
def assets_vm_delete():
	vid = request.args.get('vid')
	_is_ok, error = Assets_vms.assets_vm_delete(vid)
	if _is_ok:
	    flash('虚拟机删除成功')
	    return redirect('/assets_vm/')
	else:
	    flash('虚拟机删除失败')
	    return redirect('/assets_vm/')



@assets.route('/assets_physics/')
def assets_physics_list():
	assets_physics_list = Assets_physics.get_assets_physics()
	return render_template('assets_physics.html', assets=assets_physics_list)


@assets.route('/assets_physics/create/')
def assets_physics_create():
	_oses = Assets_physics.get_os_list()
	_idcs = get_idcs()
	return render_template('assets_physics_create.html', oses=_oses, idcs=_idcs)


@assets.route('/assets_physics/add/', methods=['post'])
def assets_physics_add():
	params = request.form
	sn = params.get('sn', '')
	pip = params.get('pip', '')
	vendor = params.get('vendor', '')
	model = params.get('model', '')
	esxi_version = params.get('esxi_version', '')
	purchase_date = params.get('purchase_date', '')
	warranty = params.get('warranty', '')
	bIdc = params.get('bIdc', '')
	bPod = params.get('bPod', '')
	bPu = params.get('bPu', '')
	cpuModel = params.get('cpuModel', '')
	pmem = params.get('pmem', '')
	_is_ok, _errors = Assets_physics.validate_physics_create(sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu)
	if _is_ok:
		Assets_physics.assets_physics_add(sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu)
		return json.dumps({'is_ok': _is_ok, 'success': '主机添加成功'})
	else:
		return json.dumps({'is_ok': _is_ok, 'error':_errors})

@assets.route('/assets_physics/modify/')
def assets_physics_modify():
	sn = request.args.get('sn','')
	_assets = Assets_physics.get_by_key('sn', sn)
	_oses = Assets_physics.get_os_list()
	_idcs = get_idcs()
	return render_template('assets_physics_modify.html', asset_physics = _assets, oses=_oses, idcs=_idcs)


@assets.route('/assets_physics/update/', methods=['post'])
def assets_physics_update():
	params = request.form
	sn = params.get('sn', '')
	pip = params.get('pip', '')
	vendor = params.get('vendor', '')
	model = params.get('model', '')
	esxi_version = params.get('esxi_version', '')
	purchase_date = params.get('purchase_date', '')
	warranty = params.get('warranty', '')
	bIdc = params.get('bIdc', '')
	bPod = params.get('bPod', '')
	bPu = params.get('bPu', '')
	cpuModel = params.get('cpuModel', '')
	pmem = params.get('pmem', '')

	_is_ok, error = Assets_physics.validate_physics_update(sn,pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu)
	if _is_ok:
		Assets_physics.assets_physics_update(sn, pip, vendor, model, esxi_version, cpuModel, pmem, purchase_date, warranty, bIdc, bPod, bPu)
		return json.dumps({'is_ok': _is_ok, 'success': '主机修改成功'})
	else:
		return json.dumps({'is_ok': _is_ok, 'error':_errors})

@assets.route('/assets_physics/delete/')
def assets_physics_delete():
	sn = request.args.get('sn','')
	_is_ok, error = Assets_physics.assets_physics_delete(sn)
	if _is_ok:
	    flash('主机删除成功')
	    return redirect('/assets_physics/')
	else:
	    flash('主机删除失败')
	    return redirect('/assets_physics/')


@assets.route('/up_vms/',methods=['post'])
def up_vms():
	_file = request.files.get('vmsFile')
	if _file:
		_filepath = '/tmp/vmsFile%s.csv' %time.time()
		_file.save(_filepath)
		_is_ok, error = Assets_import.import_vms(_filepath)
	
		if _is_ok:
			flash('文件导入成功')
			return redirect('/assets_vm/')
		else:
			flash('文件导入失败')
			return redirect('/assets_vm/')


@assets.route('/up_physics/',methods=['post'])
def up_physics():
	_file = request.files.get('physicsFile')
	if _file:
		_filepath = '/tmp/physicsFile%s.csv' %time.time()
		_file.save(_filepath)
		_is_ok, error = Assets_import.import_physics(_filepath)
	
		if _is_ok:
			flash('文件导入成功')
			return redirect('/assets_physics/')
		else:
			flash('文件导入失败')
			return redirect('/assets_physics/')

@assets.route('/assets_physics/download/')
def assets_physics_download():
	_column = 'pid,sn,pip,vendor,model,esxi_version,cpuModel,pmem,PurchaseDate,warranty,bIdc,bPod,bPu'
	_assets = Assets_physics.get_hostList()
	_columns = _column.split(',')
	fh = StringIO()
	csv_writer = csv.writer(fh)
	csv_writer.writerow(_columns)
	for _asset in _assets:
		data = []
		for col in _columns:
			data.append(_asset.get(col))
		csv_writer.writerow(data)
	cxt = fh.getvalue()
	fh.close()
	return cxt,200,{'Content-Type': 'text/csv; charset=utf-8',"Content-Disposition":"attachment;filename=physicsFile.csv"}


@assets.route('/assets_vms/download/')
def assets_vms_download():
	_column = 'vid,vmid,application,vmip,os,cpuThread,mem,disk,bHost'
	_assets = Assets_vms.get_vmList()
	_columns = _column.split(',')
	fh = StringIO()
	csv_writer = csv.writer(fh)
	csv_writer.writerow(_columns)
	for _asset in _assets:
		data = []
		for col in _columns:
			data.append(_asset.get(col))
		csv_writer.writerow(data)
	cxt = fh.getvalue()
	fh.close()
	return cxt,200,{'Content-Type': 'text/csv; charset=utf-8',"Content-Disposition":"attachment;filename=vmsFile.csv"}

