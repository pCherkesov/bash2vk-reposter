# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import datetime
import ConfigParser

class Config:
	cfg = False

	@staticmethod
	def init(file):
		if Config.cfg == False:
			cfg = ConfigParser.ConfigParser()
			cfg.read(file)
			Config.cfg = cfg

	@staticmethod
	def getCfg(charter, name):
		return Config.cfg.get(charter.upper(), name)
