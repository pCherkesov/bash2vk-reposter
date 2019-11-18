#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class Bash_comics(read.Read):

	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"comics"
		self.from_group = 1
		self.post_type = "quote"

	def getPosts(self):
		return self.__postCheck(self.__read())

	def __preCheck(self):
		pass

	def __read(self):
		tree = self._get('http://bash.im/comics')
		quotes = tree.xpath('.//article[@class = "quote strip"]/div[@class="quote__frame"]')
		for block in quotes:
			q_id = block.xpath("substring-after(div[@class='quote__footer']/div[@class='quote__author'], '#')").strip()
			self.image = 'http://bash.im' + block.xpath("div[@class='quote__body']/img[@class='quote__img']/@data-src")[0]
			break

		tree = self._get('http://bash.im/quote/' + q_id)
		q_text = '\n'.join(tree.xpath("//div[@class='quote__body']/text()")).strip()

		return {q_id: self.tag(q_text)}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)