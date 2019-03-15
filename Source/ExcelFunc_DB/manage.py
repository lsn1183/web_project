#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os

from restapi.app import app

if __name__ == '__main__':
    #app.run(debug = True)
    app.run(host='0.0.0.0')
