# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import datetime
import ConfigParser

from bash_vk import vk
from bash_vk import log
from bash_vk import base
from bash_vk import security

class Bash_vk:
	vk = False
	db = False
	lg = False
	cfg = False

	def __init__(self):
		## Load config file ###
		self.cfg = ConfigParser.ConfigParser()
		self.cfg.read('./bash.ini')

		### Load main classes ###
		self.vk = vk.Vk(self)
		self.db = base.Base(self.getCfg('BASE', 'path'))
		self.lg = log.Log()


	def log(self, msg, mtype = "message"):
		if mtype == "message":
			self.lg.screen(msg)
		elif mtype == "info":
			self.lg.screen(msg, False)


	def getCfg(self, charter, name):
		return self.cfg.get(charter.upper(), name)

	def getLastPost(self, post_type):
		return self.db.getLastPost(post_type)

	def getDate(self):
		return datetime.datetime.today()

	def checkWall(self):
		self.log("Wall scanning......", "info")

		access_users = self.getCfg('main', 'access_users')
		try:
			for post in self.getWall('others'):
				if str(post["from_id"]) not in access_users:
					self.log(self.__delWall(post["id"]))
					self.log(self.__banUser(post["from_id"]))

		except KeyError, error:
			self.log(str(error))
			return True

		return True

	# VK-API Functions
	def getWall(self, filters):
		try:
			return self.vk.getWall(50, filters)['items']
		except KeyError, error:
			self.log(str(error))
			return {}

	def delWall(self, post_id):
		return self.vk.delWall(post_id)


	def banUser(self, user_id, ban_time, reason):
		return self.vk.banUser(user_id, ban_time, reason)