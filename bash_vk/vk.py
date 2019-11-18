#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import vk_api
import datetime
import requests

from bash_vk.log import Log
from bash_vk.config import Config

class Vk:
	api = False
	session = False
	group_api = False
	group_session = False
	owner_id = ""
	group_id = ""

	postTime = 0
	postPause = 0
	postCount = {'from_group': 0, "from_user": 0}

	api_version = "5.92"

	@staticmethod
	def init(pause = 10):
		if Vk.api == False and Vk.group_api == False:
			if Config.getCfg('vk-api', 'token') is not "":
				Vk.session = vk_api.VkApi(token = Config.getCfg('vk-api', 'token'), api_version = Vk.api_version)
				Vk.api = Vk.session.get_api()

			if Config.getCfg('vk-api', 'group_token') is not "":
				Vk.group_session = vk_api.VkApi(token = Config.getCfg('vk-api', 'group_token'), api_version = Vk.api_version)
				Vk.group_api = Vk.group_session.get_api()			

			Vk.postTime = datetime.datetime.now()
			Vk.postPause = pause
			Vk.group_id = str(Config.getCfg('vk-api', 'group_id'))
			Vk.owner_id = "-" + Vk.group_id

	@staticmethod
	def getLastPost(self):
		return self.postTime

	@staticmethod
	def post(msg, from_group, attachment = False):
		if (datetime.datetime.now() - Vk.postTime) > datetime.timedelta(seconds = Vk.postPause):
			time.sleep(Vk.postPause)

		if False != attachment:
			attachment = Vk._upload(attachment)

		try:
			return Vk.api.wall.post(owner_id = Vk.owner_id, from_group = from_group, message = msg, attachments = attachment)['post_id']

		except requests.exceptions.ConnectionError as error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError as error:
			Log.log(error)
			return False
		except KeyError:
			Log.log("")
			return False

	@staticmethod
	def postComment(msg, post_id, attachment = False):
		if False != attachment:
			attachment = Vk._upload(attachment)

		try:
			return Vk.api.wall.createComment(owner_id = Vk.owner_id, from_group = Vk.group_id, post_id = post_id, message = msg, attachments = attachment)

		except requests.exceptions.ConnectionError as error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError as error:
			Log.log(error)
			return False
		except KeyError:
			Log.log("")
			return False

	@staticmethod
	def _upload(url):
		filename = "upload/" + url.split("/")[-1]

		try:
			if "http" in url:
				r = requests.get(url, stream = True)
				if r.status_code == 200:
					with open(filename, 'wb') as f:
						for chunk in r.iter_content(1024):
							f.write(chunk)

			upload = vk_api.VkUpload(Vk.session)
			photo = upload.photo_wall(filename, group_id = Vk.group_id)
		except requests.exceptions.ConnectionError as error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError as error:
			Log.log(error)
			return False

		os.remove(filename)

		return 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
		
	@staticmethod
	def getWall(count, filters):
		try:
			return Vk.api.wall.get(owner_id = Vk.owner_id, count = count, filter = filters)['items']
		except requests.exceptions.ConnectionError as error:
			Log.log(error)
		except vk_api.exceptions.ApiError as error:
			Log.log(error)

		return {}

	@staticmethod
	def delWall(post_id):
		try:
			Vk.api.wall.delete(owner_id = Vk.owner_id, post_id = post_id)
			return True
		except requests.exceptions.ConnectionError as error:
			Log.log(error)
		except vk_api.exceptions.ApiError as error:
			Log.log(error)

	@staticmethod
	def getMessages(chat_id, rev = 1, count = 1, offset = 0):
		if rev == 1:
			offset = offset + 1

		try:
			messages = Vk.group_api.messages.getHistory(user_id = chat_id, group_id = Vk.group_id, offset = offset, rev = rev, count = count)

			if len(messages) > 0 and 'count' in messages and messages['count'] > 0:
				return messages['items'][0]
			else:
				return False

		except requests.exceptions.ConnectionError as error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError as error:
			Log.log("VK.getMessages: " + str(error))
			return False


	@staticmethod
	def delMessage(msg_id, for_all = 1):
		try:
			messages = Vk.group_api.messages.delete(group_id = Vk.group_id, message_ids = msg_id, delete_for_all = for_all)
			return True

		except requests.exceptions.ConnectionError as error:
			Log.log(error)
		except vk_api.exceptions.ApiError as error:
			Log.log(error)

	@staticmethod
	def getUser(user_id, fields):
		try:
			return Vk.api.users.get(user_ids = user_id, fields = fields)

		except requests.exceptions.ConnectionError as error:
			Log.log(error)
		except vk_api.exceptions.ApiError as error:
			Log.log(error)

	@staticmethod
	def banUser(user_id, ban_time, reason):
		end_time = datetime.timedelta(seconds = time.time() + ban_time).total_seconds()
		try:
			Vk.api.groups.banUser(group_id = Vk.group_id, user_id = user_id, end_date = end_time,
									reason = 0, comment_visible = 1, comment = reason)
			return True
		except requests.exceptions.ConnectionError as error:
			Log.log(error)
		except vk_api.exceptions.ApiError as error:
			Log.log(error)
