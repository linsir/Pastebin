#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 10:19:39
# @Author  : Linsir (vi5i0n@hotmail.com)
# @Link    : http://Linsir.sinaapp.com
# @Version : $Id$
from math import ceil
from tornado.web import RequestHandler
from setting import page_size, is_debug

def get_paged(*args, **kwargs):
    "页数"
    handler = args[0]
    return int(handler.get_argument('paged', '1'))

class Page(object):
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

class BaseHandler(RequestHandler):
    """docstring for BaseHandler"""
    def write_error(self, status_code, **kwargs):
        self.finish('404 error')

    def render(self, template_name, root=None):
        kwargs = merge_dict(root, all_funcs)

        if kwargs.haskey('self'):
            del kwargs['self']
        html = self.render_string(template_name, **kwargs)
        # html += self.reques_time_info()
        self.write(html)
        
        

