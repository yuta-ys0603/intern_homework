#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import handler
from tornado.web import url

class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tornado.web.Application.__init__(self,
                                                    [
                                                    url(r'/home', handler.HomeHandler, name='home'),
                                                    url(r'/talk', handler.TalkHandler, name='talk'),
                                                    url(r'/chat', handler.ChatHandler, name='chat'),
                                                    url(r'/profile', handler.ProfileHandler, name='profile'),
                                                    url(r'/', handler.LoginHandler, name='login'),
                                                    url(r'/logout', handler.LogoutHanler, name='logout'),
                                                    url(r'/entry', handler.EntryHandler, name='entry'),
                                                    ],
            template_path = os.path.join(BASE_DIR, '../templates'),
            static_path = os.path.join(BASE_DIR, '../static'),
            login_url = '/',
            xsrf_cookies = True,
            cookie_secret = 'afasf156a48e6wag1arw56rwe4',
            debug = True,
        )

if __name__ == '__main__':
    try:
        app = Application()
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8888)
        print('Server is up')
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
