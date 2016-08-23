#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

assets = Blueprint('assets', __name__, template_folder="templates", static_folder='static')
import views 