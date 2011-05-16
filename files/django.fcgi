#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setpath
setpath.setPath()

from django.core.servers.fastcgi import runfastcgi

runfastcgi(method='threaded', daemonize='false')
