#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

idcs = Blueprint('idcs', __name__, template_folder="templates", static_folder='static')
import views 