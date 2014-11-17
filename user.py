#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-08 16:08:21
# @Author  : Linsir (vi5i0n@qq.com)
# @Link    : http://Linsir.sinaapp.com
# @Version : $Id$
from tornado.escape import xhtml_escape
from handlers import BaseHandler
from utils import get_paged, PageInfo, fmt_time, if_out
from db import *

class UserLogin(BaseHandler):    
    def post(self):
        id = self.get_argument('id', '')
        if self.check_login(id):
            self.redirect('/modify/' + str(id))
        else:
            password = self.get_argument('password', '')
            if Post.get_password(id) == password:
                self.set_secure_cookie('Codeid', id, 1)
                self.redirect('/detail/' + str(id))
            else:
                self.redirect('/')

class Modify(BaseHandler):
    def get(self, id):
        if self.check_login(id):
            post = Post.query_detail(int(id))
            self.render("modify.html", post=post, if_out=if_out)
        else:
            url = '/detail/' + str(id)
            self.redirect(url)

    def post(self,id):
        if self.check_login(id):
            id = int(id)
            url = '/detail/' + str(id)
            title = xhtml_escape(self.get_argument('title', ''))
            poster = xhtml_escape(self.get_argument('poster', ''))
            password = xhtml_escape(self.get_argument('password', ''))
            type = xhtml_escape(self.get_argument('syntax', 'other'))
            content = xhtml_escape(self.get_argument('content', ''))
            time = fmt_time()
            Post.modify(id, title, poster, type, content, time, password)
            self.redirect(url) 
        else:
            self.redirect('/detail/' + str(id))

class UserDelete(BaseHandler):
    def get(self,id):
        if self.check_login(id):
            Post.remove(int(id))
            self.clear_cookie('Codeid')
            self.redirect('/')

