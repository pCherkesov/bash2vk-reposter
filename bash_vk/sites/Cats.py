#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import shutil
import random
import ConfigParser

from .. import read
from .. import vk


class Cats(read.Read):
	tag_name = u"простокотик"

	def read(self, time):
		if not self.__checkTime(time):
			return {}

		files = os.listdir("./cats")
		if files != []:
			random.shuffle(files)
			randomImg = files[0]
			shutil.move(r'./cats/' + randomImg, r'./upload')
			self.image = randomImg

			return {randomImg: self.tag("")}

		return {}

	def __checkTime(self, lastPost):
		cfg = ConfigParser.ConfigParser()
		cfg.read('bash.ini')
		v = vk.Vk(cfg.get('VK-API', 'token'), cfg.get('VK-API', 'group_id'))

		try:
			for post in v.getWall(10, 'owner')['items']:
				if u"простокотик" in post['text'] or u"пятничныйкотик" in post['text']:
					return False
		except KeyError:
			return False

		return True