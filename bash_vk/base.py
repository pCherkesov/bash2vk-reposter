#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

class Base:
	file = False
	db = {}

	def __init__ (self, file):
		self.file = file
		self.__connectDB()

	def save (self, charter, id):
		self.db[1].execute("INSERT INTO bash (id, charter, quote) VALUES(NULL, '%s', '%s')" % (charter, id))
		self.db[0].commit()
		return True

	def __connectDB (self):
		self.db[0] = sqlite3.connect(self.file)
		self.db[1] = self.db[0].cursor()

	def __disconnectDB (self):
		self.db[0].close()

	def check (self, charter, id):
		self.db[1].execute("SELECT COUNT() FROM bash WHERE charter = '%s' AND quote = '%s'" % (charter, str(id)))
		for row in self.db[1]:
			if row[0] == 0:
				return True
			return False
