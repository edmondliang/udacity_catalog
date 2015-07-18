#!/usr/bin/python
import sys,os
import logging
logging.basicConfig(stream=sys.stderr)

PROJECT_DIR="/var/www/catalog"
activate_this = os.path.join(PROJECT_DIR, 'env/bin', 'activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0,PROJECT_DIR)

from app import app as application
