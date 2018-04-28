# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import requests
from lxml import html
from bash_vk.config import Config

class Read:
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
	}
	group_name = Config.getCfg('vk-api', 'group_name')

	def __init__(self):
		self.tag_name = u""
		self.from_group = 0
		self.post_type = "quote"
		self.post_pause = 0
		self.image = False

	def _get(self, url):
		r = requests.get(url, self.headers)
		r.encoding = "cp1251"
		return html.fromstring(r.text)

	def tag(self, text):
		return u"#" + self.tag_name + u"@" + self.group_name + "\n" + text

	def untag(self, text):
		return text.replace(u"#" + self.tag_name + u"@" + self.group_name + "\n", "")

	def getImage(self):
		x = self.image
		self.image = False
		return x

	def getFromGroup(self):
		return self.from_group

	def getType(self):
		return self.post_type

	def getPosts(self):
		raise NotImplementedError()

	def __preCheck(self, **kwargs):
		raise NotImplementedError()

	def __postCheck(self, **kwargs):
		raise NotImplementedError()
