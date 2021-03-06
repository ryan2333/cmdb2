#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import  Flask
from assets import assets
from idcs import idcs

app = Flask(__name__)

app.secret_key = 'oF\xd3I\x98\xe5\xb4\x1a\xfb\xc77\xe3\xcc,\xc2\xd2\x05\x8b\xa9\x9b\x01\xa0t\x0f\x04\x11\x19\xcd4\x96\x8d\x14'

app.register_blueprint(assets)
app.register_blueprint(idcs)

import  views