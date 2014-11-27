#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-06 15:32:42
# @Author  : Linsir (vi5i0n@hotmail.com)
# @Link    : http://Linsir.sinaapp.com
# @Version : $Id$

import time
import random
from hashlib import sha1
from math import ceil
from datetime import datetime, timedelta
from setting import paged_size

def get_paged(*args, **kwargs):
    "页数"
    handler = args[0]
    return int(handler.get_argument('paged', '1'))

class PageInfo(object):
    """docstring for Page"""
    def __init__(self, paged, total, url, paged_size=paged_size):
        self.paged = paged
        self.total = total
        self.url = url
        self.paged_size = paged_size
        self.pages = int(ceil(float(total) / float(paged_size)))
        self.pre = (paged > 1) and (paged - 1) or 1
        self.next = (paged < self.pages) and (paged + 1) or self.pages

        if '?' in url:
            self.paged_url = url + '&paged='
        else:
            self.paged_url = url + '?paged='

        self.pre_url = self.paged_url + str(self.pre)
        self.next_url = self.paged_url + str(self.next)

def encrypt(password):
    """
    加密管理员密码，使用 `pbkdf2` 加密方法
    """
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    enpasswd = sha1(sha1((salt + password).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
    return str(salt) + '$' + str(enpasswd)


def checkpassword(passwd, enpasswd):
    salt = enpasswd[:8]
    password = sha1(sha1((salt + passwd).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
    p = str(salt) + '$' + str(password)
    return (p == enpasswd)

# 当前时间戳(精确到秒)
def now():
    return int(time.time())

# 格式化时间, 默认返回当前时间
def fmt_time(fmt='%Y-%m-%d %H:%M:%S', seconds=None):
    if not seconds: seconds = now()
    t = datetime.utcfromtimestamp(seconds)
    t = t + timedelta(hours=+8) # 时区
    return t.strftime(fmt)

def if_out(flag, out):
    return flag and out or ''

if __name__ == '__main__':
    print fmt_time()
    print encrypt('admin')

