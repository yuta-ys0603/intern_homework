#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import json
import tornado.ioloop
import tornado.websocket
import do_sql
from tornado.web import url

class BaseHandler(tornado.web.RequestHandler):
    cookie_username = 'username'

    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_cuurent_user(self,username):
        self.set_secure_cookie(self.cookie_username,tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        friend_list = do_sql.DoSql.select_friends(self.current_user.decode('utf-8'))
        self.render('home.html', friend_list = friend_list)


class TalkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('talk.html')


class ChatHandler(tornado.websocket.WebSocketHandler,BaseHandler):
    waiters = set()
    messages = []

    def open(self, *args, **kwargs):
        if self.current_user not in self.waiters:
            self.waiters.add(self.current_user)
        self.write_message({'messages': self.messages})

    def on_message(self,message):
        message = json.loads(message)
        self.messages.append(message)
        for waiter in self.waiters:
            if waiter == self.current_user:
                continue
            waiter.write_message({'message':message['message']})

    def on_close(self):
        self.waiters.remove(self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        try:
            if (username,password) ==  (do_sql.DoSql.select_user(username,password)):
                self.set_cuurent_user(username)
                self.redirect('/home')
        except:
            self.redirect('/')


class LogoutHanler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_current_user()
        self.redirect('/')


class EntryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('entry.html')

    def post(self):
        try:
            username = self.get_argument('username')
            email = self.get_argument('email')
            password = self.get_argument('password')
            # do_sql.DoSql.entry_user(username,email,password) #insert to db(no protected)
            self.render('/')
        except Exception:
            self.redirect('/entry')


class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('profile.html')
