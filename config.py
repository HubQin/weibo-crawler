#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 数据库连接配置

mysql_config = {
	'host': "192.168.10.10",   # 数据库连接
	'name': "homestead",		 # 账号名称
	'password': "secret",      # 密码
	'db': "weibo",			 # 数据库名称
}

sleep_time: 3  # 每抓取一条休眠时间

# 待抓取的用户列表
users = [
	{
		"name": "测试例子",
		"uid": '123456' ,
		"value": '123456' ,
		"containerid": '123456' ,
		"is_enable": False,   # True 代表要抓取，False 不抓取
		"start_time": "2009-12-12" # 从哪个时间的微博开始抓取，格式yyyy-mm-dd，留空则使用上次抓取到的时间点, 想从头抓取，则设置一个久远的时间点
	},
	{
		"name": "纯银V",
		"uid": '1134424202',
		"value": '1134424202',
		"containerid": '1076031134424202',
		"is_enable": True,   
		"start_time": "2009-12-12"
	}
]

# 微博请求头
postsHeaders = {
	'cookie': '_ga=GA1.2.578026448.1581433612; _T_WM=93430961632; WEIBOCN_FROM=1110006030; MLOGIN=0; XSRF-TOKEN=bb6be7; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031134424202%26fid%3D1076031134424202%26uicode%3D10000011',
	'mweibo-pwa': '1',
	'referer': 'https://m.weibo.cn/u/1134424202?uid=1134424202&luicode=10000011&lfid=1076031134424202',
	'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
}


# 微博列表URL格式 
postListUrlFormat = r'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={value}&containerid={containerid}&page={page}'

# 单条微博URL格式
postUrlFormat = r'https://m.weibo.cn/statuses/extend?id={}'