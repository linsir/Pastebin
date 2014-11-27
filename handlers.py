#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 10:19:39
# @Author  : Linsir (vi5i0n@hotmail.com)
# @Link    : http://Linsir.sinaapp.com

from tornado.web import RequestHandler
from tornado.escape import xhtml_escape

from setting import paged_size, is_debug, cookie_timeout
from db import *
from utils import fmt_time, get_paged, PageInfo, if_out


class BaseHandler(RequestHandler):
    """docstring for BaseHandler"""
    def get(self):
        # raise HTTPError(404)
        self.write_error(404)
        
    def write_error(self, status_code, **kwargs):
        # self.finish('404 NOT FOUND!!' + str(status_code))
        self.render('error.html')

    def get_current_user(self):
        if is_debug: return 'debug_user'
        return self.get_secure_cookie("user")

    def check_login(self, id):
        cookie_id = self.get_secure_cookie('Codeid')
        return cookie_id == id

class Home(BaseHandler):
    def get(self):
        paged = get_paged(self)
        total, posts = Post.query(paged)
        page_info = PageInfo(paged, total, '/')
        return self.render('index.html', posts=posts, page_info=page_info, if_out=if_out)


class Detail(BaseHandler):
    def get(self, id):
        post = Post.query_detail(int(id))
        return self.render('detail.html', post=post, check_login=self.check_login(id))

class SearchByType(BaseHandler):
    def get(self, type):
        paged = get_paged(self)
        url = '/' + type + '/'
        total, posts = Post.query(paged,type)
        page_info = PageInfo(paged, total, url)
        return self.render("index.html", posts=posts, page_info=page_info, if_out=if_out)


class NewPost(BaseHandler):
    def get(self):
        self.render("new.html",)
 
    def post(self):
        title = xhtml_escape(self.get_argument('title', ''))
        poster = xhtml_escape(self.get_argument('poster', ''))
        password = xhtml_escape(self.get_argument('password', ''))
        type = xhtml_escape(self.get_argument('syntax', 'other'))
        content = xhtml_escape(self.get_argument('content', ''))
        time = fmt_time()
        Post.add(title, poster, type, content, time, password)
        self.redirect('/')

        


        

        



        
            