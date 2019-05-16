# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import json
import time
from GetCookie import *

session = requests.session()


def getJson(shop_name,shop_id, page):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://ruiducp.m.tmall.com/shop/shop_auction_search.htm?&shop_id=' + shop_id + '&sort=default',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'ruiducp.m.tmall.com'
    }
    num = str(random.randint(83739921, 87739530))
    url = "https://"+str(shop_name)+".m.tmall.com/shop/shop_auction_search.do?spm=a2141.7631565.0.0.496714bbs5vOWO&sort=s&p="+str(page)+"&page_size=12&from=h5&&shop_id="+shop_id+"ajson=1&_tm_source=tmallsearch&callback=jsonp_" + num
    cookie = getAllCookies(shop_id,session)
    r = session.get(url, headers=headers, cookies=cookie)
    html = r.text
    return html


def writeJson(html,page):
    resultJson = {}
    start = html.find('(')
    resultJson[str(page)] = json.loads(html[start + 1:-1])
    print(resultJson)
    file = open("./json", "a", encoding="utf-8")
    file.write(str(resultJson) + "\n")
    file.close()


def getAllPage(shop_name,shop_id):
    # 获取总页数
    html=getJson(shop_name,shop_id, 1)
    start = html.find('(')
    total_page = int((json.loads(html[start + 1:-1]))['total_page'])
    # 写入本地
    writeJson(html, 1)

    # 实现循环抓取
    for i in range(2, total_page + 1):
        range_html = getJson(shop_name,shop_id,i)
        # 写入本地
        writeJson(range_html, i)
        time.sleep(random.randint(2, 4))

def main():
    # 输入店铺名和店铺的id
    shop_name="ruiducp"
    shop_id = "381682363"
    getAllPage(shop_name,shop_id)


if __name__ == '__main__':
    main()
    # https://ruiducp.m.tmall.com/?shop_id=381682363
