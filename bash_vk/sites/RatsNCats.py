#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read

class RatsNCats (read.Read):
	tag_name = u"RatsNCats"
	postPause = 0

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		q_id = []
		q_text = []
		q_data = {}
		tree = self.__get('http://acomics.ru/~rats-n-cats')

		quotes = tree.xpath('.//div[@class = "quote"]')
		for block in quotes:
			q_id.append(block.xpath("substring-after(div[@class='actions']/span[@class='id'], '#')"))
			q_text.append('\n'.join(block.xpath("div[@class='text']/text()")))

		for i, q in zip(q_id, q_text):
			q_data[i] = self.tag(q)

		return q_data

	def __checkTime(self, lastPost):
		return True