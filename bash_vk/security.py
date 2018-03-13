#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import datetime

class Wall:
    api = False
    access_id = []
    checkTime = False

    def __init__(self, api, access_id):
        self.api = api
        self.access_id.append(access_id)

    def check(self):
        self.checkTime = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        sys.stdout.write("\r" + self.checkTime + " - Wall scanning...                     ")
        try:
            for post in self.api.getWall(10, 'others')['items']:
                if str(post["from_id"]) not in self.access_id:
                    sys.stdout.write(self.__delWall(post["id"]))
                    sys.stdout.write(self.__banUser(post["from_id"]), "Запрещено постить на стене группы")
        except KeyError, error:
            sys.stdout.write("\r" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + " - " + str(error) + "\n")
            return True

        return True

    def __delWall(self, post_id):
        self.api.delWall(post_id)
        sys.stdout.write("\r" + self.checkTime + "- Post #" + str(post_id) + " deleted\n")
        return True

    def __banUser(self, user_id):
        self.api.banUser(user_id, 86400)
        sys.stdout.write("\r" + self.checkTime + "- User id" + str(user_id) + " banned\n")
        return True
