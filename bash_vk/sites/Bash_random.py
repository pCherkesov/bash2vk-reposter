#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import datetime

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class Bash_random(read.Read):

	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"Случайные"
		self.from_group = 1
		self.post_type = "quote"
		self.post_pause = 60

	def getPosts(self):
		if not self.__preCheck(Base.getLastPost4Type(self.post_type)):
			return {}

		return self.__postCheck(self.__read())


	def __preCheck(self, lastPost):
		if (datetime.datetime.now() - datetime.datetime.strptime(lastPost, "%Y-%m-%d %H:%M:%S")) > datetime.timedelta(minutes = self.post_pause):
			return True
		return False

	def __read(self):
		q_id = []
		q_text = []
		q_data = {}

		tree = self._get('http://bash.im/random')
		quotes = tree.xpath('.//article[@class = "quote"]/div[@class="quote__frame"]')

		for block in quotes:
			if (block.xpath("substring-after(header[@class='quote__header']/a[@class='quote__header_permalink'], '#')") != ""):
				q_date = block.xpath(u"substring-before(header[@class='quote__header']/div[@class='quote__header_date'], ' в')").strip()
				if int(q_date[6:10]) < int('{:%Y}'.format(datetime.datetime.now())) - 10:
					q_id.append(block.xpath("substring-after(header[@class='quote__header']/a[@class='quote__header_permalink'], '#')"))
					q_text.append('\n'.join(block.xpath("div[@class='quote__body']/text()")).strip() + u"\n\n" + u"Цитата от " + q_date)

		for i, q in zip(q_id, q_text):
			q_data[i] = q

		randomId = random.choice(list(q_data.keys()))
		q_data[randomId] = self.tag(q_data[randomId])

		return {randomId: q_data[randomId]}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)
