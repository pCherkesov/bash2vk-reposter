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
		quotes = tree.xpath('.//div[@class = "quote"]')

		for block in quotes:
			if (block.xpath("substring-after(div[@class='actions']/a[@class='id'], '#')") != ""):
				q_date = block.xpath("substring-before(div[@class='actions']/span[@class='date'], ' ')")
				if int(q_date[:4]) < int('{:%Y}'.format(datetime.datetime.now())) - 4:
					q_id.append(block.xpath("substring-after(div[@class='actions']/a[@class='id'], '#')"))
					q_text.append(
						'\n'.join(block.xpath("div[@class='text']/text()")) + u"\n\n" + u"Цитата от " + q_date)

		for i, q in zip(q_id, q_text):
			q_data[i] = q

		randomId = random.sample(q_data, 1)[0]
		q_data[randomId] = self.tag(q_data[randomId])

		return {randomId: q_data[randomId]}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)