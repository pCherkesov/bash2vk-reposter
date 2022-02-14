#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class RatsNCats (read.Read):
	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"RatsNCats"
		self.from_group = 1
		self.post_type = "image"

	def getPosts(self):
		return self.__postCheck(self.__read())

	def __preCheck(self):
		pass

	def __read(self):
		q_id = []
		q_text = []
		q_data = {}
		tree = self._get('http://acomics.ru/~rats-n-cats')

		try:
			self.image = "https://acomics.ru/" + tree.xpath("//img[@id='mainImage']/@src")[0]
		except IndexError:
			return {}

		site, slash, filename = self.image.rpartition('/')

		return {filename: self.tag('')}

	def __postCheck(self, quotes):
		return Base.checkPostsList(quotes, self.__class__.__name__)