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

		q_id = tree.xpath("//span[@class='backlink']/a/@href")[1].replace("/quote/", "")
		self.image = tree.xpath("//img[@id='cm_strip']/@src")[0]

		tree = self._get('http://bash.im/quote/' + q_id)
		q_text = '\n'.join(tree.xpath("//div[@class='text']/text()"))

		return {q_id: self.tag(q_text)}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)