#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

from bash_vk import log

class Base:
	file = False
	db = {}

	def __init__ (self, file):
		self.file = file
		self.__connectDB()

	def __del__ (self):
		self.db[1].execute("VACUUM;")
		self.db[1].execute("REINDEX;")
		self.__disconnectDB()

	def createBase (self, name):
		self.db[1].execute("""CREATE TABLE IF NOT EXISTS `%s` (
			id INTEGER PRIMARY KEY, 
			from_group INTEGER DEFAULT 0, 
			charter CHARACTER, 
			post_id CHARACTER, 
			post_type CHARACTER DEFAULT 'quote', 
			post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);""" % (name))
		self.db[0].commit()
		return True

	def delBase (self, name):
		self.db[1].execute("DROP TABLE IF EXISTS `%s`;" % (name))
		self.db[0].commit()
		return True

	def execute (self, query):
		self.db[1].executescript(query)
		self.db[0].commit()
		return True

	def saveRow (self, name, data):
		self.db[1].executemany("INSERT INTO `%s` (charter, post_id) VALUES(?, ?)" % (name), data)
		self.db[0].commit()
		return True

	def readBase (self, name):
		base = []
		self.db[1].execute("SELECT charter, quote FROM `%s`" % (name))
		for row in self.db[1]:
			base.append(row)

		return base

	def setGroup (self, charter):
		self.db[1].execute("UPDATE `bash_vk` SET `from_group` = 1 WHERE `charter` = ?;", (charter, ))
		self.db[0].commit()
		return True

	def setType (self, charter, ctype):
		self.db[1].execute("UPDATE `bash_vk` SET `post_type` = ? WHERE `charter` = ?;", (ctype, charter))
		self.db[0].commit()
		return True

	def convertCharter (self, old, new):
		self.db[1].execute("UPDATE `bash` SET `charter` = ? WHERE `charter` = ?;", (new, old))
		self.db[0].commit()
		return True

	def __connectDB (self):
		self.db[0] = sqlite3.connect(self.file)
		self.db[1] = self.db[0].cursor()

	def __disconnectDB (self):
		self.db[0].close()


b = Base("bash.db")

log = log.Log()

name = "Base bash_vk converter v 0.1"
log.screen(name)
log.screen("=" * len(name))


log.screen("Convert charter")
charters = {u"Bash_im": u"Главная", u"Bash_random": u"Случайные", u"Bash_best": u"ЛучшееБездны", u"Bash_comics": u"comics" }
for new, old in charters.iteritems():
	b.convertCharter(old, new)

log.screen("Create new base")
b.createBase('bash_vk')

log.screen("Read old base")
quotes = b.readBase('bash')

log.screen("Save new base")
b.saveRow('bash_vk', quotes)

log.screen("Delete old base")
b.delBase('bash')

log.screen("Insert from_group value in new base")
b.setGroup(u"Bash_im")
b.setGroup(u"Bash_random")
b.setGroup(u"Bash_comics")

log.screen("Insert type value in new base")
b.setType(u"Bash_comics", u"image")

log.screen("Convert base DONE")

del b