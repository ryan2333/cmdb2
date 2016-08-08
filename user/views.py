#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import app
from flask import render_template, request, redirect

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


@app.route('/login/', methods=['post', 'get'])
def login():
	username = request.form.get('username', '')
	password = request.form.get('password', '')


if __name__ == '__main__':
	import utils
	utils