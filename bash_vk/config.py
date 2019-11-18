# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import datetime
from configparser import ConfigParser

class Config:
	cfg = False

	@staticmethod
	def init(file):
		if Config.cfg == False:
			cfg = ConfigParser()
			cfg.read(file)
			Config.cfg = cfg

	@staticmethod
	def getCfg(charter, name):
		return Config.cfg.get(charter.upper(), name)


class BashReadError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)