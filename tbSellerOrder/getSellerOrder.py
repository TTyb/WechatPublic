#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json
import demjson
from prettytable import PrettyTable

header = {}
header['user-agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36'
header['referer'] = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'

cookies = {}
cookiestr = '''
            (cookie)
            '''

for cookie in cookiestr.split(';'):
    name, value = cookie.strip().split('=', 1)
    cookies[name] = value

def getOrder():
    url = "https://trade.taobao.com/trade/itemlist/list_sold_items.htm"

    try:
        response = requests.post(url, headers=header, cookies=cookies)
        content = None

        if response.status_code == requests.codes.ok:
            content = response.text
    except Exception as e:
        print(e)
    data = json.loads(reg(content))

    if data.get('mainOrders'):
        getOrderDetails(data.get('mainOrders'))
    else:
        print("error")


# 正则获取json
def reg(html):
    reg = r'(JSON.parse\(\')(.+?)(\'\))'
    all = re.compile(reg)
    alllist = re.findall(all, html)
    return alllist[0][1].replace('\\"','"')

def getOrderDetails(data):
    table = PrettyTable()
    table.field_names = ["ID", "卖家", "名称", "订单创建时间", "价格", "状态"]

    for order in data:
        tmp = []
        # id =
        tmp.append(order.get('id'))
        # shopName
        tmp.append(order.get('buyer').get('nick'))
        # title
        tmp.append(order.get('subOrders')[0].get('itemInfo').get('title'))
        # createTime
        tmp.append(order.get('orderInfo').get('createTime'))
        # actualFee
        tmp.append(order.get('payInfo').get('actualFee'))
        # text
        tmp.append(order.get('statusInfo').get('text'))

        table.add_row(tmp)

    print(table)


if __name__ == '__main__':
    getOrder()