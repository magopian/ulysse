#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Set paths

If the project folder contains a 'venv' folder, setPath makes sure that
venv/lib/pythonx.x/site-packages is used as the default path.

"""

import os
import site
import sys

# applications are stored in the django project folder
_PROJECT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# folder containing the django project itself
_ROOT = os.path.dirname(_PROJECT)
_NAME = os.path.basename(_PROJECT)

# two first numbers of the version, ie python2.6
_SHORTVER = "python%s.%s" % (sys.version_info[0], sys.version_info[1])

# optional virtualenv site-packages directory.
_LIB = 'lib/%s/site-packages' % _SHORTVER
_VENV = os.path.join(_PROJECT, 'venv', _LIB)

def setPath():
    prev_sys_path = list(sys.path)
    site.addsitedir(_VENV)
    sys.path.append(_ROOT)
    sys.path.append(_PROJECT)

    # reorder sys.path so new directories from the addsitedir show up first
    new_sys_path = [p for p in sys.path if p not in prev_sys_path]
    for item in new_sys_path:
        sys.path.remove(item)
    sys.path[:0] = new_sys_path

    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % _NAME

