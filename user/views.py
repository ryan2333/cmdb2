#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

from . import app
from functools import wraps
from flask import render_template, request, redirect, session, flash
from models import User,UserType
import json

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')

        rt = func(*args, **kwargs)
        return rt

    return wrapper


@app.route('/')  #将url path=/的请求交由index函数处理
def index():
    return render_template('login.html')


def userType():
    user_type=UserType.get_user_types()
    print user_type
    return user_type


@login_required
@app.route('/users/')
def user_list():
    _user = User.get_users()
    return render_template('users.html', users=_user)


@app.route('/login/', methods=['post', 'get'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    _user = User.validate_login(username, password)
    if _user:
        session['user'] = _user
        return redirect('/users/')
    else:
        return render_template('login.html', username=username, error='用户名或密码错误')


@login_required
@app.route('/user/create/')
def user_create():
    return render_template('user_create.html', userType=userType())


@login_required
@app.route('/user/add/', methods=['post'])
def user_add():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    reppassword = request.form.get('passwordrep', '')
    email = request.form.get('email', '')
    usertype = request.form.get('usertype', 0)

    _is_ok, _errors = User.validate_user_add(username,password,reppassword)

    if _is_ok:
        User.user_add(username,password,email,usertype)
        return json.dumps({'is_ok': _is_ok, 'success': '用户创建成功','error':_errors})
    else:
        return json.dumps({'is_ok': _is_ok, 'error':_errors})


@login_required
@app.route('/user/modify/')
def user_modify():
    uid = request.args.get('uid', '')
    _user = User.get_user_by('uid', uid)
    return render_template('user_modify.html', users=_user, usertype=userType())


@login_required
@app.route('/user/update/', methods=['post'])
def user_update():
    uid = request.form.get('userid', '')
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    usertype = request.form.get('usertype', 0)
    _is_ok, errors = User.user_update(uid, username, email, usertype)
    if _is_ok:
        return json.dumps({'is_ok':_is_ok, 'success':'用户信息更新成功'})
    else:
        return json.dumps({'is_ok':_is_ok, 'error':'用户信息更新失败'})


@login_required
@app.route('/user/delete/')
def user_delete():
    uid = request.args.get('uid','')
    username = request.args.get('username','')
    _is_ok, errors = User.user_delete(uid, username)
    if _is_ok:
        flash('用户删除成功')
        return redirect('/users/')
    else:
        flash('用户删除失败')
        return redirect('/users/')


@login_required
@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
	import utils
	utils