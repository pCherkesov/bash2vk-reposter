# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import requests
from lxml import html

class Read:
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
	}
	tag_name = False
	postPause = 0
	image = False

	def _get(self, url):
		r = requests.get(url, self.headers)
		r.encoding = "cp1251"
		return html.fromstring(r.text)

	def tag(self, text):
		return u"#" + self.tag_name + u"@all_bor\n" + text

	def untag(self, text):
		return text.replace(u"#" + self.tag_name + u"@all_bor\n", "")

	def getImage(self):
		x = self.image
		self.image = False
		return x

	def read(self, time):
		raise NotImplementedError()


	def __check(self, lastPost):
		raise NotImplementedError()