#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 10:56:31
# @Author  : Linsir (vi5i0n@qq.com)
# @Link    : http://Linsir.sinaapp.com
# @Version : $Id$

import sqlite3
from setting import data_file, paged_size

class _Post(object):
    """docstring for _Post"""
    def __init__(self):
        self.data_file = data_file
        self.conn = sqlite3.connect(data_file)
        self.cur = self.conn.cursor()

    def query(self, paged, type=None, paged_size=paged_size,):
        
        sql = 'SELECT * FROM posts ' 
        total_sql = 'SELECT count(*) FROM posts'
        if type:
            sql += ' WHERE type="%s"' %type
            total_sql += ' WHERE type="%s"' %type
        sql = sql + 'ORDER BY id DESC LIMIT %s OFFSET %s ' %(paged_size, (paged - 1) * paged_size)
        self.cur.execute(total_sql)
        total = self.cur.fetchone()[0]
        self.cur.execute(sql)
        posts = self.cur.fetchall()
        return total, posts

    def query_detail(self, id):
        
        sql = 'SELECT * FROM posts WHERE id=%d' %id
        self.cur.execute(sql)
        post = self.cur.fetchone()
        
        return post

    def add(self, title, poster, type, content, time, password=''):
        sql = '''INSERT INTO posts(title, poster, type, content, time, password) \
        values("%s","%s","%s","%s","%s","%s")''' %(title, poster, type, content, time, password)
        # print sql
        self.cur.execute(sql)
        self.conn.commit()

    def modify(self, id, title, poster, type, content, time, password):
        sql = 'UPDATE posts SET title="%s", poster="%s", type="%s", content="%s", time="%s",\
         password="%s" WHERE id=%s' %(title, poster, type, content, time, password, id)
        self.cur.execute(sql)
        self.conn.commit()

    def remove(self, id):
        sql = 'DELETE FROM posts WHERE id=%s' %id
        self.cur.execute(sql)
        self.conn.commit()

    def get_password(self,id):
        sql = 'SELECT password FROM posts WHERE id=%s' %id
        self.cur.execute(sql)
        return self.cur.fetchone()[0]

    def __del__(self):
        self.cur.close
        self.conn.close

Post = _Post()

class _Admin(object):
    def __init__(self):
        self.data_file = data_file
        self.conn = sqlite3.connect(data_file)
        self.cur = self.conn.cursor()

    def get_username(self):
        sql = 'SELECT user FROM admin'
        self.cur.execute(sql)
        user = self.cur.fetchone()[0]
        return user

    def get_password(self):
        sql = 'SELECT password FROM admin'
        self.cur.execute(sql)
        password = self.cur.fetchone()[0]
        return password

    def __del__(self):
        self.cur.close
        self.conn.close

Admin = _Admin()

all_funcs = locals()

if __name__ == '__main__':
    # for post in query(1)[1]:
    #     print post
    Post.add('ahaha', 'tomebkeeper', 'java', 'ahahahha', '20101010','123')
    # print Post.query(1,)
    print Admin.get_username()
    print Post.get_password(1)

    pass

