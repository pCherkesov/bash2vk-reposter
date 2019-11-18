#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read
# from bash_vk.vk import Vk
from bash_vk.base import Base

class site_sample(read.Read):
	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"Sample-site"
		self.from_group = 1
		self.post_type = "quote"

	def getPosts(self):
		if not self.__preCheck():
			return {}

		read = self.__read()

		return self.__postCheck(read)

	def __preCheck(self):
		return True

	def __read(self):
		# url at image
		self.image = False

		# Return dict with id quotes as key, and text quotes as data
		return {'key': self.tag('value')}

	def __postCheck(self, quotes):
		return quotes