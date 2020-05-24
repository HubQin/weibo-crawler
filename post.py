#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
post.py
~~~~~~~~~~~~~~~~~
Crawl post content
"""
import requests  
import json
from bs4 import BeautifulSoup
from config import *
from database import Db
from gadget import *
import time

# 微博爬虫
class PostCrawler(object):
    def __init__(self):
        pass

    # 获取每一页数据
    def getPage(self, db, user, page):
        # url = postListUrlFormat.format(uid = user['uid'], value = user['value'], containerid = user['containerid'], page = page)
        url = 'https://m.weibo.cn/api/container/getIndex?uid=1134424202&luicode=10000011&lfid=1076031134424202&type=uid&value=1134424202&containerid=1076031134424202&since_id=4507392476551679'

        data = requests.get(url, headers = postsHeaders)
        data.encoding = 'utf-8'
        data = json.loads(data.text)
        return data

    def parseCard(self, content, user, latestTimestamp):
        if('mblog' in content.keys()):
            addTime = getTimestamp(content['mblog']['created_at'])
            print('微博添加时间%s' % addTime)

            if addTime > latestTimestamp:

                if db.postExists(user['uid'], content['mblog']['id'], 'posts'):
                    print('POST ID: %s 已在数据库中，跳过\n' % content['mblog']['id'])
                    return None

                print('POST ID: %s 开始抓取\n' % content['mblog']['id'])
                kwPost = {}
                kwPost['user_id'] = user['uid']
                kwPost['add_time'] = addTime
                kwPost['post_id'] = content['mblog']['id'] 
                kwPost['attitudes_count'] = content['mblog']['attitudes_count'] 
                kwPost['comments_count'] = content['mblog']['comments_count']

                # if there is not long text, use the current text,otherwise get the long text
                if content['mblog']['isLongText'] == False:
                    kwPost['content'] = content['mblog']['text']
                else:
                    kwPost['content'] = self.getLongTextContent(content['mblog']['id'])

                # if fail to get long text, just use the short one instead
                if kwPost['content'] == False:
                        kwPost['content'] = content['mblog']['text']

                # if has retweeted content, get it in the same way
                if 'retweeted_status' in content['mblog']:
                    kwPost['retweet_id'] = content['mblog']['retweeted_status']['id']
                    # if there is not long text, use the current text,otherwise get the long text
                    if content['mblog']['retweeted_status']['isLongText'] == False:
                        kwPost['retweet_content'] = content['mblog']['retweeted_status']['text']
                    else:
                        kwPost['retweet_content'] = self.getLongTextContent(content['mblog']['retweeted_status']['id'])
                    # if fail to get long text, use the short one instead
                    if kwPost['retweet_content'] == False:
                        kwPost['retweet_content'] = content['mblog']['retweeted_status']['text']

                # 返回组装好的数据
                return kwPost

            else:
                print('发表时间在设置的或上次抓取的时间之前，不写入')
                return None
        else:
            return None

    def getLongTextContent(self, id):
        url = postUrlFormat.format(id)
        data = requests.get(url, headers = postsHeaders)
        if data and '打开微博客户端' not in data.text:
            data.encoding = 'utf-8'
            data = json.loads(data.text)
            return data['data']['longTextContent']
        else:
            return False

if __name__ == '__main__':

    db = Db()
    postCrawler = PostCrawler()

    printUserInfo(users)

    for user in users:

        if user['is_enable'] == False:
            print('%s 用户设置为不抓取，跳过...\n' % user['name'])
            continue

        # 获取起始时间点
        latestTimestamp = getStartTime(user)
        
        page = 1

        timeLocal = getDate(latestTimestamp)
        print("=====开始抓取用户：%s,时间:[%s]之后的微博=====\n" % (user['name'], timeLocal))

        while True:
            print("=====开始抓取第%s页的微博=====" % page)
            
            try: 
                pageData = postCrawler.getPage(db, user, page)

                if pageData and len(pageData['data']['cards']):
                    for card in pageData['data']['cards']:
                        result = postCrawler.parseCard(card, user, latestTimestamp)
                        if result:
                            # 如果有符合条件的微博，写入数据库
                            db.insert_data('posts', **result)
                else:
                    print('该页数已没有内容, 接着抓取下一个用户...\n')
                    break

            except Exception as e:
                print("结束抓取用户：%s，第%s页，原因：%s\n" % (user['name'], page, e))
                break

            page = page + 1
            time.sleep(3)
