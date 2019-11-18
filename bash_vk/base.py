#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sqlite3

class Base:
	file = False
	cursor = False
	connect = False

	@staticmethod
	def init(file):
		Base.__connectDB(file)

	@staticmethod
	def close():
		Base.cursor.execute("VACUUM;")
		Base.cursor.execute("REINDEX;")

	@staticmethod
	def __createBase():
		Base.cursor.execute("""
				CREATE TABLE bash_vk (
				ID INTEGER PRIMARY KEY,
				charter CHARACTER,
				post_id CHARACTER,
				post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);
		""")
		Base.connect.commit()
		return True

	@staticmethod
	def __connectDB(file):
		if os.path.isfile(file):
			Base.connect = sqlite3.connect(file)
			Base.cursor = Base.connect.cursor()
		else:
			Base.connect = sqlite3.connect(file)
			Base.cursor = Base.connect.cursor()
			Base.__createBase()

	@staticmethod
	def __disconnectDB():
		Base.connect.close()

	@staticmethod
	def counts(date):
		Base.cursor.execute("SELECT count() FROM `bash_vk` WHERE DATE(`post_time`) = ? GROUP BY `from_group`;", (date, ))
		counts = Base.cursor.fetchall()
		return {"from_user": counts[0][0], "from_group": counts[1][0]}

	@staticmethod
	def getLastPost4Type(post_type):
			Base.cursor.execute("SELECT DATETIME(MAX(`post_time`), 'localtime') FROM `bash_vk` WHERE `post_type` = ?;", (post_type, ))
			return Base.cursor.fetchall()[0][0]

	@staticmethod
	def getLastPost4Name(charter):
			Base.cursor.execute("SELECT DATETIME(MAX(`post_time`), 'localtime') FROM `bash_vk` WHERE `charter` = ?;", (charter, ))
			return Base.cursor.fetchall()[0][0]

	@staticmethod
	def savePost(charter, post_type, post_id):
		Base.cursor.execute("INSERT INTO `bash_vk` (charter, post_type, post_id) VALUES (?, ?, ?)", (charter, post_type, post_id))
		Base.connect.commit()
		return True

	@staticmethod
	def checkPostsList(quotes, charter):
		for id, quote in sorted(quotes.items()):
			Base.cursor.execute("SELECT COUNT() FROM `bash_vk` WHERE charter = ? AND post_id = ?", (charter, str(id)))
			for row in Base.cursor:
				if row[0] != 0:
					quotes.pop(id)

		return quotes

