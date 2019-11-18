#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bash_vk.vk import Vk
from bash_vk.log import Log
from bash_vk.config import Config

class Security:
    access_id = []

    @staticmethod
    def init():
        Security.access_id.append(Config.getCfg("security", "access_users"))

    @staticmethod
    def check():
        Log.log("Wall scanning......", "info")
        try:
            for post in Vk.getWall(10, 'others'):
                if str(post["from_id"]) not in Security.access_id:
                    Log.log(Security.__delWall(post["id"]))
                    Log.log(Security.__banUser(post["from_id"]))
        except KeyError as error:
            Log.log(str(error))
            return True

        return True

    @staticmethod
    def __delWall(post_id):
        Vk.delWall(post_id)
        return "Post #" + str(post_id) + " deleted"

    @staticmethod
    def __banUser(user_id):
        Vk.banUser(user_id, 86400, u"Запрещено постить на стене группы")
        return "User id" + str(user_id) + " banned"
