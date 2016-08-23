#!/usr/bin/env python
# -*- coding: utf-8 -*-

from idcs import idcs
from flask import render_template, request, flash, redirect
import json
from model import Idcs,Oses,UserType



@idcs.route('/idcs/')
def idcs_list():
	_idcs = Idcs.get_idc_list()
	return render_template('idcs.html', idcs=_idcs)


@idcs.route('/idcs/create/')
def idcs_create():
	return render_template('idcs_create.html')


@idcs.route('/idcs/add/',methods=['post'])
def idcs_add():
	params = request.form
	idcName = params.get('idcname','')
	pods = params.get('idcpods','')
	bandwidth = params.get('bandwidth',10)
	t_contact = params.get('t-contact','')
	t_phone = params.get('t-contact','')
	kf_contact = params.get('kf-contact','')
	kf_phone = params.get('kf-phone','')
	start_date = params.get('startdate','')
	address = params.get('address','')
	_is_ok,error = Idcs.validate_idc_add(idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,address)
	if _is_ok:
		_is_ok,error = Idcs.idc_add(idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address)
		return json.dumps({'is_ok':_is_ok, 'success':'机房添加成功'})
	else:
		return json.dumps({'is_ok':_is_ok, 'error':'\n'.join(error)})


@idcs.route('/idcs/modify/')
def idcs_modify():
	_id = request.args.get('sn','')
	_idcs = Idcs.get_by_id('id',_id)
	return render_template('idcs_modify.html', idcs=_idcs)


@idcs.route('/idcs/update/',methods=['post'])
def idcs_update():
	params = request.form
	_id = params.get('id','')
	idcName = params.get('idcname','')
	pods = params.get('idcpods','')
	bandwidth = params.get('bandwidth',10)
	t_contact = params.get('t-contact','')
	t_phone = params.get('t-phone','')
	kf_contact = params.get('kf-contact','')
	kf_phone = params.get('kf-phone','')
	start_date = params.get('startdate','')
	address = params.get('address','')
	_is_ok,error = Idcs.validate_idc_update(pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,address)
	if _is_ok:
		_is_ok,error = Idcs.idc_update(_id,idcName,pods,bandwidth,t_contact,t_phone,kf_contact,kf_phone,start_date,address)
		return json.dumps({'is_ok':_is_ok, 'success':'机房信息修改成功'})
	else:
		return json.dumps({'is_ok':_is_ok, 'error':'\n'.join(error)})

@idcs.route('/idcs/delete/')
def idcs_delete():
	_id = request.args.get('id','')
	_is_ok,error = Idcs.idc_delete(_id)

	if _is_ok:
		flash('机房删除成功')
		return redirect('/idcs/')
	else:
		flash('机房删除失败')
		return redirect('/idcs/')

@idcs.route('/oses/')
def oses_list():
	_os_list = Oses.get_oses_list()
	return render_template('oses.html',oses=_os_list)

@idcs.route('/oses/create/')
def oses_create():
	return render_template('os_create.html')

@idcs.route('/oses/add/',methods=['post'])
def oses_add():
	_osname = request.form.get('osname','')
	_is_ok,error = Oses.validate_os_add(_osname)
	if _is_ok:
		_is_ok,error = Oses.oses_add(_osname)
		return json.dumps({'is_ok':_is_ok, 'success':'操作系统添加成功'})
	else:
		return json.dumps({'is_ok':_is_ok, 'error':error})

@idcs.route('/oses/delete/')
def oses_delete():
	_id = request.args.get('id','')
	_is_ok,error = Oses.oses_delete(_id)
	if _is_ok:
		flash('系统删除成功')
		return redirect('/oses/')
	else:
		flash('系统删除失败')
		return redirect('/oses/')

@idcs.route('/user_types/')
def usertypes():
	_usertypes = UserType.get_usertype_list()
	return render_template('usertype.html',usertypes=_usertypes)



@idcs.route('/usertype/create/')
def usertype_create():
	return render_template('usertype_create.html')


@idcs.route('/usertype/add/',methods=['post'])
def usertype_add():
	tname = request.form.get('tname','')
	_is_ok,error = UserType.validate_usertype_add(tname)
	if _is_ok:
		_is_ok,error = UserType.usertype_add(tname)
		return json.dumps({'is_ok':_is_ok, 'success':'用户类型添加成功'})
	else:
		return json.dumps({'is_ok':_is_ok, 'error':error})

@idcs.route('/usertype/delete/')
def usertype_delete():
	tid = request.args.get('tid','')
	_is_ok,error = UserType.usertype_delete(tid)
	if _is_ok:
		flash('系统删除成功')
		return redirect('/user_types/')
	else:
		flash('系统删除失败')
		return redirect('/user_types/')

