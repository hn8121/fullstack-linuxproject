#!/usr/bin/env python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, "/var/www/catalog/catalog/")

from __init__ import app as application

application.secret_key = 'please_work_for_me'
