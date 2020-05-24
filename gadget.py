#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gadget.py
~~~~~~~~~~~~~~~~~
一些公用函数
"""

import time
import datetime
import os

def getTimestamp(text):
    '''Get timestamp from giving text'''

    if '刚刚' in text:
        return int(time.time())
    elif '小时' in text:
        text = text.replace('小时前', '').strip()
        seconds = int(text)*3600
        return int(time.time()) - seconds
    elif '分钟' in text:
        text = text.replace('分钟前', '').strip()
        seconds = int(text)*60
        return int(time.time()) - seconds
    elif '昨天' in text:
        text = text.replace('昨天','').strip()
        timeArray = text.split(':')
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        timeStruct = time.strptime(str(yesterday),'%Y-%m-%d')
        timestamp = int(time.mktime(timeStruct))
        timestamp = timestamp + int(timeArray[0]) * 3600 + int(timeArray[1]) * 60
        return timestamp
    else:
        # 今年比较远的日期，是以m-d表示的，补全年份先
        if text.count('-') == 1:
            text = str((datetime.datetime.now()).year) + '-' + text

        # 包含有时和分的
        if ':' in text and ' ' in text:
            timeStruct = time.strptime(text,'%Y-%m-%d %H:%M')
        # 年月日表示的
        else:
            timeStruct = time.strptime(text,'%Y-%m-%d')
        # 转为时间戳
        timestamp = int(time.mktime(timeStruct))
        return timestamp

def getDate(timestamp):
    '''Transform timestamp to date'''
    
    timeLocal = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",timeLocal)
    return dt


def saveLastTimestamp(timestamp,filename):
    if not os.path.exists('log'):
        os.mkdir('log')
    with open('log/'+filename,'a',encoding='utf-8') as f:
        f.write('保存时间：'+str(datetime.datetime.now())+'\t开始时间戳：'+str(timestamp)+'\n')
        f.close()

def saveFailId(id,title):
    if not os.path.exists('log'):
        os.mkdir('log')
    with open('log/weibo_article_fail_id.txt','a',encoding='utf-8') as f:
        f.write(title+'\t'+str(id)+'\n')
        f.close()

def getStartTime(user):
    # 如果有设置时间点 使用设置的
    if user['start_time']:
        latestTimestamp = getTimestamp(user['start_time'])
    else:
        # 否则使用最近一次抓取到的时间点
        latestTimestamp = db.selectLastCrawlerTime(user['uid'],'posts')
    # 数据库也没有记录，设为0
    if latestTimestamp == None:
        latestTimestamp = 0
    return latestTimestamp

def printUserInfo(users):
    print("抓取的用户列表：\n")
    for user in users:
        print("用户名：%s 是否抓取：%s, 时间点：%s\n" % (user['name'], user['is_enable'], user['start_time']))
