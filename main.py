# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import time
from os import listdir
from importlib import import_module

from bash_vk.vk import Vk
from bash_vk.log import Log
from bash_vk.base import Base
from bash_vk.config import Config
from bash_vk.security import Security

### Load main classes ###
Config.init('./bash.ini')
Base.init('bash.db')
Vk.init()
Security.init()

### DRATUTI ###
Log.log(Config.getCfg('MAIN', 'program') + " v." + Config.getCfg('MAIN', 'version'))
Log.log("=" * len(Config.getCfg('MAIN', 'program') + " v." + Config.getCfg('MAIN', 'version')))

### Dynamic load parsing classes from bash_vk\sites ###
classes = []
files = listdir(".\\bash_vk\\sites")
sites = filter(lambda x: x.endswith('.py'), files)
sites = filter(lambda x: x != "__init__.py", sites)
sites = filter(lambda x: x != "site_sample.py", sites)
sites = map(lambda x: x[:-3], sites)

for charter in sites:
	module = import_module("bash_vk.sites." + charter)
	classes.append(getattr(module, charter)())
	Log.log("Load module: " + charter)

### MAIN LOOP ###
while 1 == 1:
	for charter in classes:
		Log.log('Scanning ' + charter.__class__.__name__ + '......', "info")
		q = charter.getPosts()

		for id, quote in sorted(q.iteritems()):
			post = Vk.post(quote, charter.getFromGroup(), charter.getImage())
			if False != post:
				Base.savePost(charter.__class__.__name__, charter.getType(), id)
				Log.log(charter.__class__.__name__ + " add post: " + str(id) + " (vk id: " + str(post) + ")")

		time.sleep(30)
		Security.check()
		time.sleep(5)