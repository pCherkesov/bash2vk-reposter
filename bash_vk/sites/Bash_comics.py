#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read

class Bash_comics (read.Read):
	tag_name = u"comics"
	postPause = 0

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		tree = self._get('http://bash.im/comics')

		q_id = tree.xpath("//span[@class='backlink']/a/@href")[1].replace("/quote/", "")
		self.image = tree.xpath("//img[@id='cm_strip']/@src")[0]

		tree = self._get('http://bash.im/quote/' + q_id)
		q_text = '\n'.join(tree.xpath("//div[@class='text']/text()"))

		return {q_id: q_text}

	def __checkTime(self, lastPost):
		return True