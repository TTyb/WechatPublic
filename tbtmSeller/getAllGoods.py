# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import json
import time
from GetCookie import *
import math


def getJson(shop_name, shop_id, page):
    num = str(int(time.time() * 1000) % 100000) + str(math.ceil(random.random() * 1000))
    url = "https://"+str(shop_name)+".m.tmall.com/shop/shop_auction_search.do?sort=s&p="+str(page)+"&page_size=12&from=h5&shop_id="+str(shop_id)+"&ajson=1&_tm_source=tmallsearch&callback=jsonp_" + num
    # url = "https://ruiducp.m.tmall.com/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&shop_id=381682363&ajson=1&_tm_source=tmallsearch&callback=jsonp_" + num
    print(url)
    session = requests.session()
    # 这里可以不用生成的cookie，可以用自己得到的cookie
    cookie = getAllCookies(shop_name,shop_id,session)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Host': str(shop_name) + '.m.tmall.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'
    }

    r = session.get(url, headers=headers,cookies=cookie)
    print(r.request.headers)
    print(r.history)
    print(r.status_code)
    html = r.text
    return html


def writeJson(html, page):
    resultJson = {}
    start = html.find('(')
    resultJson[str(page)] = json.loads(html[start + 1:-1])
    print(resultJson)
    file = open("./json", "a", encoding="utf-8")
    file.write(str(resultJson) + "\n")
    file.close()


def getAllPage(shop_name, shop_id):
    # 获取总页数
    html = getJson(shop_name, shop_id, 1)
    print(html)
    start = html.find('(')
    total_page = int((json.loads(html[start + 1:-1]))['total_page'])
    # 写入本地
    writeJson(html, 1)

    # 实现循环抓取
    for i in range(2, total_page + 1):
        range_html = getJson(shop_name, shop_id, i)
        # 写入本地
        writeJson(range_html, i)
        time.sleep(random.randint(2, 4))


def main():
    # 输入店铺名和店铺的id
    shop_name = "ruiducp"
    shop_id = "381682363"
    getAllPage(shop_name, shop_id)


if __name__ == '__main__':
    main()
    # https://ruiducp.m.tmall.com/?shop_id=381682363
