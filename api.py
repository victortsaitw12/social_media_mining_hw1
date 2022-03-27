#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time

class Api:

    def __init__(self, domain, loadsecond):
        self.domain = domain
        self.intermit=loadsecond
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/59.0.3071.115 Safari/537.36'}

    def goto(self, path):
        print('goto', path)
        resp = requests.get(self.domain + path, headers=self.headers).json()
        self.sleep()
        return resp

    def sleep(self, sec=None):
        if sec is None:
            second=self.intermit
        time.sleep(second)
