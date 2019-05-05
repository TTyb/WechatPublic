#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import json

session = requests.session()


# 获取商品ID
def get_id_json(page, keyword):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://uland.taobao.com/semm/tbsearch?refpid=mm_26632258_3504122_32554087&keyword=%E5%A5%B3%E8'
                   '%A3%85 '
                   '&rewriteQuery=1&a=mi={imei}&sms=baidu&idfa={'
                   'idfa}&clk1=abab6283306413775910d4b0b37ca047&upsid=abab6283306413775910d4b0b37ca047',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
    }

    url = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID%2CRANKINFO%2CMATCHTYPE&pvid=_TL' \
          '-41832&refpid=mm_26632258_3504122_32554087&clk1=abab6283306413775910d4b0b37ca047&idfa=%7Bidfa%7D&pid' \
          '=430680_1006&keyword=' + keyword + '&count=60&offset=' + str(60 * page) + '&relacount=8&t=1535075213992' \
                                                                                     '&callback' \
                                                                                     '=mn17jsonp1535075213992 '
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['result']['item']
    return datas


# 获取评论
def getComment(resource_id):
    url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=10&pageSize=20"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://item.taobao.com/item.htm?id=590983542794&ali_refid=a3_430125_1006:1110717877:N:iphonex%E6%89%8B%E6%9C%BA%E5%A3%B3:ebb2e8948bfcf1ac8c57f88cb9a352ed&ali_trackid=1_ebb2e8948bfcf1ac8c57f88cb9a352ed'
                   '&rewriteQuery=1&a=mi={imei}&sms=baidu&idfa={'
                   'idfa}&clk1=abab6283306413775910d4b0b37ca047&upsid=abab6283306413775910d4b0b37ca047',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'cookie': 'isg=BKqqA-P4gquQvA7H4wA4IwUk-BBMGy51PVpFXDRjVv2oZ0shHKoQhTbR91VejKYN; l=bBxAccLIvDBT78OhBOCa-urza77THIObYuPzaNbMi_5wv6YfRNbOlBlE8Fv6V_CP9lLB4oIS68JthemYJyMf.; cna=M4dVFcAGRTMCAQ4dfkRPitl6; t=8f9ebc97b652309cd0a7523a197f28a9; _m_h5_tk=de3500c1e15b8951fb3b24f1e850a903_1557052077140; _m_h5_tk_enc=462aca9d8ea739408f685a5d40997fd3; enc=GtoW8paBYDMyf5qiqn0SHlkWQ%2BcxW4Wp3XpF6Z9sggD337wKmKWA1vathW%2BJXqLHripJk2X9Vtlqw4xmEVYsdg%3D%3D; cookie2=1c2a5c099615ce110ddfea30dccf0f8d; v=0; _tb_token_=b911e365e0ed; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; mt=ci%3D-1_1; uc1=cookie14=UoTZ48X3fEGxKg%3D%3D'
    }

    r = session.get(url=url, headers=headers)
    print(r.text)
    # 评论数
    total = json.loads(r.text.strip().strip('()'))['total']
    count = 0
    page = 1
    """
    try:
        while count < total:
            url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=" + str(page) + "&pageSize=20"
            r = session.get(url=url, headers=headers)
            page = page + 1
            comments = json.loads(r.text.strip().strip('()'))['comments']
            for comment in comments:
                print(comment)
                count = count + 1
            time.sleep(5)
    except Exception as e:
        print(e)
        print(r.content)
    """

def getJsonData(page, keyword):
    for item in range(0, page):
        datas = get_id_json(page + 1, keyword)
        for item in datas:
            resource_id = item["RESOURCEID"]
            getComment(resource_id)

if __name__ == "__main__":
    page = 10
    keyword = "iphone x".replace(" ", "+")
    getJsonData(page, keyword)
