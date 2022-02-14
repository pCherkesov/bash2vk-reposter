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
		self.codebase = "CP1251"

	def getPosts(self):
		if not self.__preCheck(Base.getLastPost4Name(self.__class__.__name__)):
			return {}

		return self.__postCheck(self.__read())


	def __preCheck(self, lastPost):
		if (datetime.datetime.now() - datetime.datetime.strptime(lastPost, "%Y-%m-%d %H:%M:%S")) > datetime.timedelta(hours = self.post_pause):
			return True
		return False

	def __read(self):
		tree = self._get('http://ibash.org.ru/random.php')

		try:
			q_id = tree.xpath("substring-after(//div[@class='quothead']/span/a/b, '#')")
			q_text = '\n'.join(tree.xpath("//div[@class='quotbody']/text()"))
			q_date = tree.xpath("//div[@class='quinfo']/span/text()")[1].split(" ")[2]
			q_text = q_text + u"\n\n" + u"Цитата от " + q_date
		except IndexError:
			return {}

		return {q_id: self.tag(q_text)}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)
