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


# 获取评论，通过携带登录过后的cookie
def getCommentByCookie(resource_id):
    url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=10&pageSize=20"
    headers = {
        "cookie": "miid=292998242037415425; t=a210415a1655c0232f82eb7b3a6104df; UM_distinctid=166ceb653b3579-076dd76f89438e-b79183d-100200-166ceb653b4311; cna=bbxhFGBja3gCAW8e7cIps2En; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=%5Cu68A6%5Cu4E00%5Cu6837%5Cu81EA%5Cu7531101; lgc=%5Cu68A6%5Cu4E00%5Cu6837%5Cu81EA%5Cu7531101; tg=0; ubn=p; ucn=center; enc=UIB9oC%2F4GcT7MT%2BeTYYspmIzgCQGQVgVtIdOafyHPB%2FddpEQuoTVRFhD3T2%2B4ZTQppw07b1yUBPdsBcmiZRl0Q%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; mt=ci=34_1&np=; _m_h5_tk=ab92273cd1f1994a79de75803c72eedd_1542899769491; _m_h5_tk_enc=9af4f2d58367798bd6fd9fc571623a03; v=0; cookie2=1e3e736fa27ece822d8e0584a52fc0e2; _tb_token_=e3e5b95fa56e5; unb=2193645594; sg=142; _l_g_=Ug%3D%3D; skt=6dfe74172437c7ae; cookie1=AVS2RlAz2mIjdZAY7fy%2BfYtP4kUpRn3V%2FbBr8i8CU%2BA%3D; csg=934ced39; uc3=vt3=F8dByR6oLTybe7NAPL0%3D&id2=UUkHLXG%2BJ1%2FZ%2BQ%3D%3D&nk2=oHTbYBpzsOUZCkBrgQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTU0Mjg5MjM3NQ%3D%3D; _cc_=WqG3DMC9EA%3D%3D; dnk=%5Cu68A6%5Cu4E00%5Cu6837%5Cu81EA%5Cu7531101; _nk_=%5Cu68A6%5Cu4E00%5Cu6837%5Cu81EA%5Cu7531101; cookie17=UUkHLXG%2BJ1%2FZ%2BQ%3D%3D; swfstore=183268; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=W5iHLLyFe3xm&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTYNOeMOTy2Mw%3D%3D&cart_m=0&tag=8&lng=zh_CN; isg=BJ6eJxdPST-Vf513tvmQfSZu7zQg92O0wyXss0gnR-Hcaz9FsO_g6NBJZxdC01rx",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive'
    }

    r = session.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    try:
        # 评论数
        total = json.loads(r.text.strip().strip('()'))['total']
        count = 0
        page = 1
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

# 获取评论，不携带cookie
def getComment(resource_id):
    pass

def getJsonData(page, keyword):
    for item in range(0, page):
        datas = get_id_json(page + 1, keyword)
        for item in datas:
            resource_id = item["RESOURCEID"]
            getCommentByCookie(resource_id)


if __name__ == "__main__":
    page = 10
    keyword = "iphone x".replace(" ", "+")
    getJsonData(page, keyword)
