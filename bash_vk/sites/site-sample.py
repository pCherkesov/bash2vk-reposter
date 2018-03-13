#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read

class site-sample (read.Read):
	tag_name = u"Sample"

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		# url at image
		self.image = False

		# Return dict with id quotes as key, and text quotes as data
		return {}

	def __checkTime(self, lastPost):
		return True