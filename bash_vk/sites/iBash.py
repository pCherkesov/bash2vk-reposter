#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime

from .. import read

class iBash (read.Read):
	tag_name = u"ibash"
	postPause = 60

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		q_id = []
		q_text = []
		q_data = {}
		tree = self._get('http://ibash.org.ru/random.php')

		quotes = tree.xpath('.//div[@class = "quote"]')
		for block in quotes:
			q_id.append(block.xpath("substring-after(div[@class='quothead']/span/a/b, '#')"))
			q_text.append('\n'.join(block.xpath("div[@class='quotbody']/text()")))

		for i, q in zip(q_id, q_text):
			q_data[i] = self.tag(q)

		return q_data

	def __checkTime(self, lastPost):
		if (datetime.datetime.now() - lastPost) > datetime.timedelta(minutes = self.postPause):
			return True
		return False