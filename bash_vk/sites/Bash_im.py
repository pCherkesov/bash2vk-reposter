#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class Bash_im(read.Read):
	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"Главная"
		self.from_group = 1
		self.post_type = "quote"

	def getPosts(self):
		return self.__postCheck(self.__read())

	def __preCheck(self):
		pass

	def __read(self):
		q_id = []
		q_text = []
		q_data = {}

		tree = self._get('http://bash.im')
		quotes = tree.xpath('.//article[@class = "quote"]/div[@class="quote__frame"]')

		for block in quotes:
			q_id.append(block.xpath("substring-after(header[@class='quote__header']/a[@class='quote__header_permalink'], '#')"))
			q_text.append('\n'.join(block.xpath("div[@class='quote__body']/text()")).strip())

		for i, q in zip(q_id, q_text):
			q_data[i] = self.tag(q)

		return q_data

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)