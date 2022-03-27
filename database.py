#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import time

class Database:
    def __init__(self, connection, db):
        self._client = pymongo.MongoClient(connection)
        self._db = self._client[db]

    def insert(self, collection, data):
        return self._db[collection].update_one({'_id': data['_id']}, {'$set': data}, upsert=True)

    def find(self, collection, data):
        return self._db[collection].find_one({'_id': data['_id']})

    def findById(self, collection, _id):
        return self._db[collection].find_one({'_id': _id})

    def findAll(self, collection):
        return self._db[collection].find()
