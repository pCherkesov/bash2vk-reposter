#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import datetime

class Log:
	@staticmethod
	def log(msg, ltype = "message"):
		if ltype == "message":
			Log.screen(msg)
		elif ltype == "info":
			Log.screen(msg, False)

	@staticmethod
	def screen (msg, new = True):
		line = '{:%Y-%m-%d %H:%M:%S} - '.format(datetime.datetime.now()) + str(msg) + " " * (100 - len(str(msg)))

		if new is not False:
			line = line + "\n"

		sys.stdout.write("\r" + line)
		return True

	@staticmethod
	def getDate():
		return datetime.datetime.today()

	@staticmethod
	def getDateTime():
		return datetime.datetime.now()