#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import vk_api
import datetime
import requests

class Vk:
	api = False
	session = False
	owner_id = ""
	group_id = ""
	from_group = 1

	postTime = 0
	postPause = 10
	postCount = {'from_group': 0, "from_user": 0}

	def __init__(self, token, group_id, from_group = 1, pause = 10):
		self.session = vk_api.VkApi(token = token, api_version = "5.73")
		self.api = self.session.get_api()

		self.postPause = pause
		self.group_id = str(group_id)
		self.owner_id = "-" + self.group_id
		self.from_group = from_group
		self.postTime = datetime.datetime.now()

	def getLastPost(self):
		return self.postTime

	def post(self, msg, attachment = False):
		if (datetime.datetime.now() - self.postTime) > datetime.timedelta(seconds = self.postPause):
			time.sleep(self.postPause)

		if False != attachment:
			attachment = self._upload(attachment)

		try:
			return self.api.wall.post(owner_id = self.owner_id, from_group = self.from_group, message = msg, attachments = attachment)['post_id']
		except requests.exceptions.ConnectionError, error:
			self.__errorMsg(error)
			return False
		except vk_api.exceptions.ApiError, error:
			self.__errorMsg(error)
			return False
		except KeyError:
			return False

	def _upload(self, url):
		filename = "upload/" + url.split("/")[-1]

		try:
			if "http" in url:
				r = requests.get(url, stream=True)
				if r.status_code == 200:
					with open(filename, 'wb') as f:
						for chunk in r.iter_content(1024):
							f.write(chunk)

			upload = vk_api.VkUpload(self.session)
			photo = upload.photo_wall(filename, group_id = self.group_id)
		except requests.exceptions.ConnectionError, error:
			self.__errorMsg(error)
			return {}
		except vk_api.exceptions.ApiError, error:
			self.__errorMsg(error)
			return {}

		os.remove(filename)

		return 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])

	def getWall(self, count, filters):
		try:
			return self.api.wall.get(owner_id = self.owner_id, count = count, filter = filters)
		except requests.exceptions.ConnectionError, error:
			self.__errorMsg(error)
			return {}
		except vk_api.exceptions.ApiError, error:
			self.__errorMsg(error)
			return {}

	def delWall(self, post_id):
		try:
			self.api.wall.delete(owner_id = self.owner_id, post_id = post_id)
			return "OK"
		except requests.exceptions.ConnectionError, error:
			self.__errorMsg(error)
			return False
		except vk_api.exceptions.ApiError, error:
			self.__errorMsg(error)
			return False

	def banUser(self, user_id, ban_time, reason):
		end_time = datetime.timedelta(seconds = time.time() + ban_time).total_seconds()
		try:
			self.api.groups.banUser(group_id = self.group_id, user_id = user_id, end_date = end_time,
											reason = 0, comment_visible = 1, comment = reason)
			return "OK"
		except requests.exceptions.ConnectionError, error:
			self.__errorMsg(error)
			return False
		except vk_api.exceptions.ApiError, error:
			self.__errorMsg(error)
			return False

	def __errorMsg(self, msg):
		sys.stdout.write("\r" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + " - " + str(msg) + "\n")