#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import datetime

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class Ipfw_random(read.Read):

	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"ipfw"
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

		tree = self._get('http://ipfw.ru/bash/random')
		quotes = tree.xpath('.//div[@class="quote"]')

		for block in quotes:
			header = block.xpath("div[@class='quotheader']")[0]
			q_date = header.xpath("substring-before(span[@class='appdate'], ' ')")
			q_id.append(header.xpath("span[@class='quotnumber']/a/text()")[0])
			q_text.append('\n'.join(block.xpath("div[@class='quotebody']/text()")) + u"\n\n" + u"Цитата от " + q_date)

		for i, q in zip(q_id, q_text):
			q_data[i] = q

		randomId = random.choice(list(q_data.keys()))
		q_data[randomId] = self.tag(q_data[randomId])

		return {randomId: q_data[randomId]}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)