#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
database.py
~~~~~~~~~~~~~~~~~
Encapsule some database operations in pymysql
"""

import pymysql

from config import mysql_config as db

class Db(object):
    """ 数据库操作类 """
    def __init__(self):
        # 初始化连接实例
        self.conn = self.db_connector()

    # 获取连接实例
    def db_connector(self):
        try:
            conn = pymysql.connect(db['host'], db['name'], db['password'], db['db'], use_unicode = True, charset="utf8mb4")
            return conn
        except Exception as e:
            print("数据库连接失败，原因：%s" % e)
            exit()

    # 插入数据
    def insert_data(self, table_name, **kw):
        # Concat SQL string which format like:"INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        sql = "INSERT INTO %s" % table_name
        sql += " ("
        tail_part = "VALUES ("
        value_list = []

        for key,value in kw.items():
            sql += "`" + key +"`,"
            tail_part += "%s,"
            value_list.append(value)

        sql = sql[:-1]
        sql += ") "

        tail_part = tail_part[:-1]
        tail_part += ")"

        # Need a tuple as parameter
        value_tuple = tuple(value_list)
        sql = sql + tail_part

        #Insert data into table
        self.conn.cursor().execute(sql,value_tuple)
        self.conn.commit()

    # 查询出上次抓取到的最近的时间点
    def selectLastCrawlerTime(self, uid, table):
        sql =  "SELECT add_time FROM `%s` WHERE user_id=%s order by add_time desc limit 1" % (table, uid)
        cur = self.conn.cursor() 
        cur.execute(sql)
        
        if cur.rowcount:
            res = self.convertDataToDict(cur)
            return res['add_time']
        else:
            return None

    # 查询对应用户的某个ID的微博是否存在
    def postExists(self, uid, post_id, table):
        sql =  "SELECT id FROM `%s`  WHERE `user_id`=%s AND `post_id`=%s LIMIT 1" % (table, uid, post_id)
        cur = self.conn.cursor() 
        cur.execute(sql)
        print(cur.rowcount)
        return bool(cur.rowcount)

    # 关闭连接
    def closeConn(self):
        self.conn.close()


    # 转换一条结果为字典
    def convertDataToDict(self, cur):
        return dict(zip([x[0] for x in cur.description],[x for x in cur.fetchone()]))

