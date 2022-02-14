#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import shutil
import random

from bash_vk.vk import Vk
from bash_vk.log import Log

class Joke():

	@staticmethod
	def post(post_id):
		if False == os.path.exists('./jokes'):
			return False
		
		if random.randint(0, 10) == 1:
			Vk.postComment("", post_id, Joke.__read())
			Log.log("Post joke comment")
			return True

		return False

	@staticmethod
	def __read():
			files = os.listdir("./jokes")
			if files != []:
				randomImg = random.choice(files)
				shutil.copy(r'./jokes/' + randomImg, r'./upload')
				return randomImg
