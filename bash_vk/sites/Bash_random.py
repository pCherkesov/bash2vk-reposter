#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import datetime

from .. import read

class Bash_random (read.Read):
	tag_name = u"Случайные"
	postPause = 60

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		q_id = []
		q_text = []
		q_data = {}
		tree = self.__get('http://bash.im/random')

		quotes = tree.xpath('.//div[@class = "quote"]')
		for block in quotes:
			if (block.xpath("substring-after(div[@class='actions']/a[@class='id'], '#')") != ""):
				q_date = block.xpath("substring-before(div[@class='actions']/span[@class='date'], ' ')")
				if int(q_date[:4]) < int('{:%Y}'.format(datetime.datetime.now())) - 4:
					q_id.append(block.xpath("substring-after(div[@class='actions']/a[@class='id'], '#')"))
					q_text.append(
						'\n'.join(block.xpath("div[@class='text']/text()")) + u"\n\n" + u"Цитата от " + q_date)

		for i, q in zip(q_id, q_text):
			q_data[i] = q

		randomId = random.sample(q_data, 1)[0]
		q_data[randomId] = self.tag(q_data[randomId])

		return {randomId: q_data[randomId]}

	def __checkTime(self, lastPost):
		if (datetime.datetime.now() - lastPost) > datetime.timedelta(minutes = self.postPause):
			return True
		return False