#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class iBash (read.Read):
	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"ibash"
		self.from_group = 1
		self.post_type = "quote"
		self.post_pause = 6

	def getPosts(self):
		if not self.__preCheck(Base.getLastPost4Name(self.__class__.__name__)):
			return {}

		return self.__postCheck(self.__read())


	def __preCheck(self, lastPost):
		if (datetime.datetime.now() - datetime.datetime.strptime(lastPost, "%Y-%m-%d %H:%M:%S")) > datetime.timedelta(hours = self.post_pause):
			return True
		return False

	def __read(self):
		q_id = []
		q_text = []
		q_data = {}
		tree = self._get('http://ibash.org.ru/random.php')

		quotes = tree.xpath('.//div[@class = "quote"]')
		for block in quotes:
			q_id.append(block.xpath("substring-after(div[@class='quothead']/span/a/b, '#')"))
			q_text.append('\n'.join(block.xpath("div[@class='quotbody']/text()")))

		for i, q in zip(q_id, q_text):
			q_data[i] = self.tag(q)

		return q_data

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)