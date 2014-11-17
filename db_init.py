#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import random
from utils import fmt_time, encrypt
from setting import data_file

class Data_init(object):
    """docstring for data_init"""
    def __init__(self):
        self.data_file = data_file
        self.conn = sqlite3.connect(data_file)
        self.cur = self.conn.cursor()

    def create_table(self):
        try:
            self.cur.execute('CREATE TABLE admin(id INTEGER PRIMARY KEY, user VARCHAR(30), password VARCHAR(50))')
            self.cur.execute('CREATE TABLE posts(id INTEGER PRIMARY KEY,title VARCHAR(50), poster VARCHAR(30), \
                type VARCHAR(20), content TEXT, time VARCHAR(20), password VARCHAR(30))')
            self.conn.commit()
        except :
            return False
        return True
    def set_admin_password(self, username="admin",password="admin"):
        self.cur.execute('DELETE FROM admin')
        sql =  '''INSERT INTO admin(user, password) values("%s", "%s")''' %(username, encrypt(password))
        self.cur.execute(sql)
        self.conn.commit()

    def test_data(self):
        types = ['Python', 'Ruby', "Lua","CSS","Java","JavaScript"]
        for i in range(0,100,5):
            title = str(i) + ".Pastebin_for_test_code"
            type = random.choice(types)
            time = fmt_time()
            sql = 'INSERT INTO posts(title, poster, type, content, time, password) \
            values("%s", "test", "%s", "#!/usr/bin/env python","%s","1")' %(title, type, time)
            self.cur.execute(sql)
            self.conn.commit()
        
    def __del__(self):
        self.cur.close
        self.conn.close
        

if __name__ == '__main__':
    username = "admin"
    password = "admin"
    data = Data_init()
    if data.create_table():
        data.set_admin_password(username, password)
        data.test_data()
    else:
        data.set_admin_password(username, password)
        # data.test_data()  

