# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import sys
import time
import datetime
import ConfigParser
from os import listdir
from importlib import import_module

from bash_vk import vk
from bash_vk import base
from bash_vk import security

## Load config file ###
cfg = ConfigParser.ConfigParser()
cfg.read('bash.ini')

### DRATUTI ###
print cfg.get('MAIN', 'program') + " v." + cfg.get('MAIN', 'version')
print "=" * len(cfg.get('MAIN', 'program') + " v." + cfg.get('MAIN', 'version'))
print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' - Start script'

### Load main classes ###
v = vk.Vk(cfg.get('VK-API', 'token'), cfg.get('VK-API', 'group_id'), from_group = 1, pause = 10)
b = base.Base(cfg.get('BASE', 'path'))
w = security.Wall(v, cfg.get('VK-API', 'access_users'))

### Dynamic load parsing classes from bash_vk\sites ###
classes = []
files = listdir(".\\bash_vk\\sites")
sites = filter(lambda x: x.endswith('.py'), files)
sites = filter(lambda x: x != "__init__.py", sites)
sites = filter(lambda x: x != "site-sample.py", sites)
sites = map(lambda x: x[:-3], sites)

for charter in sites:
	modulename, dot, classname = ("bash_vk.sites." + charter + "." + charter).rpartition('.')
	module = import_module(modulename)
	classes.append(getattr(module, classname)())


### MAIN LOOP ###
while 1 == 1:
	for charter in classes:
		sys.stdout.write('\r' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' - Scanning ' + charter.__class__.__name__ + '......      ')
		q = charter.read(v.getLastPost())

		for id, quote in sorted(q.iteritems()):
			if b.check(charter.__class__.__name__, id):
				post = v.post(quote, charter.getImage())
			else: continue

			if False != post:
				b.save(charter.__class__.__name__, id)
				sys.stdout.write("\r" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + \
								 " - " + charter.__class__.__name__ + " add quote: " + str(id) + " (post: " + str(post) + ") " + \
								 "\n")

		time.sleep(30)
		w.check()
		time.sleep(5)