#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.jianshu.com/p/8b6b3f26d089
import requests
import json
import time
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


def getOnePageOrderHistory(pageNum):
    url = "https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm"
    payload = {
        'action': 'itemlist/BoughtQueryAction',
        'event_submit_do_query': 1,
        '_input_charset': 'utf8'
    }
    formdata = {
        'pageNum': pageNum,
        'pageSize': 15,
        'prePageNo': pageNum - 1
    }

    try:
        response = requests.post(url, headers=header, params=payload, data=formdata, cookies=cookies)
        content = None

        if response.status_code == requests.codes.ok:
            content = response.text

    except Exception as e:
        print(e)

    # 成功直接获取订单
    data = json.loads(content)
    print(data)
    if data.get('mainOrders'):
        getOrderDetails(data.get('mainOrders'))
    else:
        print("error")


# 打印订单信息
def getOrderDetails(data):
    table = PrettyTable()
    table.field_names = ["ID", "卖家", "名称", "订单创建时间", "价格", "状态"]

    for order in data:
        tmp = []
        # id =
        tmp.append(order.get('id'))
        # shopName
        tmp.append(order.get('seller').get('shopName'))
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
    for i in range(2, 25):
        getOnePageOrderHistory(i)
        print("抓取第{0:d}页。".format(i))
        time.sleep(2)