#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .. import read

class Bash_best (read.Read):
	tag_name = u"Лучшее"

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		q_id = []
		q_text = []
		q_data = {}
		tree = self._get('http://bash.im/abyssbest')

		quotes = tree.xpath('.//div[@class = "quote"]')
		for block in quotes:
			q_id.append(block.xpath("substring-after(div[@class='actions']/span[@class='id'], '#')"))
			q_text.append('\n'.join(block.xpath("div[@class='text']/text()")))

		for i, q in zip(q_id, q_text):
			q_data[i] = self.tag(q)

		return q_data

	def __checkTime(self, lastPost):
		return True