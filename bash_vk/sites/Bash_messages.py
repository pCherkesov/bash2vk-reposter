#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

import random
import datetime

from .. import read
from bash_vk.vk import Vk
from bash_vk.log import Log
from bash_vk.base import Base
from bash_vk.config import Config

class Bash_messages(read.Read):
	def	__init__(self):
		read.Read.__init__(self)
		self.tag_name = u"простокотик"
		self.from_group = 1
		self.post_type = "image"

		self.users_id = Config.getCfg('bash_messages', 'users_id').split(',')

	def getPosts(self):
		if not self.__preCheck():
			return {}

		read = self.__read()

		return self.__postCheck(read)

	def __preCheck(self):
		for post in Vk.getWall(15, 'owner'):
			if "attachments" in post:
				if (datetime.datetime.now() - datetime.timedelta(minutes=240)) < datetime.datetime.fromtimestamp(post["date"]):
					return False

		return True

	def __read(self):
		randomChat = (random.choice(self.users_id))
		item = Vk.getMessages(randomChat, rev = 1, count = 1)

		if item is not False:
			if item['attachments'] == [] and item['fwd_messages'] == []:
				Vk.delMessage(item['id'], for_all = 0)
				Log.log("Message #" + str(item['id']) + " in #" + str(self.chat_id) + " chat not forward - deleted")
				return {}

			if item['attachments'] != []:
				self.image = item['attachments'][0]['photo']['sizes'][-1]['url']
				tag = u""

			if item['fwd_messages'] != []:
				self.image = item['fwd_messages'][0]['attachments'][0]['photo']['sizes'][-1]['url']
				username = Vk.getUser(item['fwd_messages'][0]['from_id'], "first_name_gen, last_name_gen")[0]
				tag = u"от @id%s (%s %s)" % (username['id'], username['first_name_gen'], username['last_name_gen'])

			Vk.delMessage(item['id'], for_all = 0)

			return {'key': self.tag(tag)}

		return {}

	def __postCheck(self, quotes):
		return quotes