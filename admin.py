#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 18:01:38
# @Author  : Linsir (vi5i0n@hotmail.com)
# @Link    : http://Linsir.sinaapp.com


from tornado.web import authenticated

from setting import cookie_timeout
from db import *
from handlers import BaseHandler
from utils import checkpassword, get_paged, PageInfo, if_out

class Login(BaseHandler):

    def _check_login(self):
        cookie_user = self.get_secure_cookie('user')
        right_user = Admin.get_username()
        return cookie_user == right_user

    def get(self):
        if self._check_login():
            self.redirect('/admin')
        else:
            html = self.render('login.html',)
        
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '/admin')
        if Admin.get_username() == username and  checkpassword(password, Admin.get_password()):
            self.set_secure_cookie('user', username, cookie_timeout)
            self.redirect(next_url)
        else:
            self.redirect('/login')

class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')

class PostList(BaseHandler):
    @authenticated
    def get(self):
        paged = get_paged(self)
        total, posts = Post.query(paged)
        page_info = PageInfo(paged, total, '/admin')
        return self.render('admin.html', posts=posts, page_info=page_info, if_out=if_out)

    def post(self):
        pass

class PostDelete(BaseHandler):
    @authenticated
    def get(self, id):
        Post.remove(int(id))
        self.redirect('/admin')
        



