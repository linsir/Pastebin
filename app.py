#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 09:48:49
# @Author  : Linsir (vi5i0n@qq.com)
# @Link    : http://Linsir.sinaapp.com
# @Version : $Id$

import os
import tornado.ioloop
import tornado.web
from handlers import *
from admin import *
from user import *
settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'gzip': True,
    'xsrf_cookies': True,
    "autoescape": None,
    'cookie_secret': 'asslkjdlkjslkdlkdkjlskjldkjlskjdl',
    'login_url': '/login',

}


handlers = [
    (r'/static/(.+)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r'/', Home),
    (r'/detail/(\d+)', Detail),
    (r'/(.+)/', SearchByType),
    (r'/new', NewPost),

    (r'/user/login', UserLogin),
    (r'/modify/(\d+)', Modify),
    (r'/delete/(\d+)', UserDelete),

    (r'/login', Login),
    (r'/logout', Logout),
    (r'/admin', PostList),
    (r'/admin/delete/(\d+)', PostDelete),
    (r'/.*', BaseHandler),
]


application = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()