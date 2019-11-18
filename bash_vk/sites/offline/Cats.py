#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import shutil
import random
import datetime

from .. import read
from bash_vk.vk import Vk
# from bash_vk.base import Base

class Cats(read.Read):

	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"простокотик"
		self.from_group = 1
		self.post_type = "image"
		self.post_pause = 240

	def getPosts(self):
		if not self.__preCheck():
			return {}

		read = self.__read()

		if False != read:
			return {read: self.tag("")}
		return {}

	def __preCheck(self):
		for post in Vk.getWall(15, 'owner'):
			if "attachments" in post:
				if (datetime.datetime.now() - datetime.timedelta(minutes = self.post_pause)) < datetime.datetime.fromtimestamp(post["date"]):
					return False

		return True

	def __read(self):
		files = os.listdir("./cats")
		if files != []:
			random.shuffle(files)
			randomImg = files[0]
			shutil.move(r'./cats/' + randomImg, r'./upload')
			self.image = randomImg
			return randomImg

		return False

	def __postCheck(self):
		pass