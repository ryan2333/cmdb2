#!/usr/bin/env python
# -*- coding: utf-8 -*-

from user import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)