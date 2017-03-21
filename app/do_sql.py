#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sqlite3

class DoSql:

    def __init__(self):
        self.result = None

    def select_user(name,password):
        con = sqlite3.connect('sqlite3.db')
        cur = con.cursor()
        cur.execute(("SELECT * FROM users WHERE name = '%s' AND password = '%s'") % (name,password))
        for row in cur:
            result = row
        con.close()

        return (result[1],result[3])

    def select_friends(name):
        friend_list = []
        con = sqlite3.connect('sqlite3.db')
        cur = con.cursor()
        cur.execute(("SELECT friend FROM friends WHERE name = '%s'") % (name))
        for row in cur:
            friend_list.append(row[0])
        con.close()

        return friend_list

    def entry_user(name,email,password):
        con = sqlite3.connect('sqlite3.db')
        cur = con.cursor()
        cur.execute(("INSERT INTO users VALUES ('%s','%s','%s')") % (name,email,password)) #need to protect
        con.commit()
        con.close()
