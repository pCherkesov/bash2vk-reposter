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
	owner_id = ""
	group_id = ""

	postTime = 0
	postPause = 0
	postCount = {'from_group': 0, "from_user": 0}

	@staticmethod
	def init(pause = 10):
		if Vk.api == False:
			Vk.session = vk_api.VkApi(token = Config.getCfg('vk-api', 'token'), api_version = "5.73")
			Vk.api = Vk.session.get_api()

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

		except requests.exceptions.ConnectionError, error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError, error:
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
		except requests.exceptions.ConnectionError, error:
			Log.log(error)
			return False
		except vk_api.exceptions.ApiError, error:
			Log.log(error)
			return False

		os.remove(filename)

		return 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
	@staticmethod
	def getWall(count, filters):
		try:
			return Vk.api.wall.get(owner_id = Vk.owner_id, count = count, filter = filters)['items']
		except requests.exceptions.ConnectionError, error:
			Log.log(error)
		except vk_api.exceptions.ApiError, error:
			Log.log(error)

	@staticmethod
	def delWall(post_id):
		try:
			Vk.api.wall.delete(owner_id = Vk.owner_id, post_id = post_id)
			return True
		except requests.exceptions.ConnectionError, error:
			Log.log(error)
		except vk_api.exceptions.ApiError, error:
			Log.log(error)

	@staticmethod
	def banUser(user_id, ban_time, reason):
		end_time = datetime.timedelta(seconds = time.time() + ban_time).total_seconds()
		try:
			Vk.api.groups.banUser(group_id = Vk.group_id, user_id = user_id, end_date = end_time,
									reason = 0, comment_visible = 1, comment = reason)
			return True
		except requests.exceptions.ConnectionError, error:
			Log.log(error)
		except vk_api.exceptions.ApiError, error:
			Log.log(error)
