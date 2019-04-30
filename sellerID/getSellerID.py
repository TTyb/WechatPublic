#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import hashlib
import json

header = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=099d87ed80b8f819245aee821810d220&keyword=%E7%BE%8E%E9%A3%9F&page=0',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/%s Mobile Safari/537.36',
    'host': 'h5api.m.taobao.com'
}

session = requests.session()


def get_m_h5_tk():
    token_url = "https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.5&appKey=12574478&t=1556611694443&sign=50cb9beadacdc7006b25feb28f687d7e&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp6&data={}"

    session.get(token_url, headers=header)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    # {'_m_h5_tk_enc': '9892c6f2340c27da4a11e6f5c7aa72e7', '_m_h5_tk': 'd655f00ac54282e4d01bc6c49a3d8cfd_1556625593335'}
    return html_set_cookie

# 获取秘钥
def get_sign(data):
    t = str(int(time.time() * 1000))
    # t = "1556617499306"
    appkey = "12574478"
    set_cookie = get_m_h5_tk()
    token = set_cookie["_m_h5_tk"].split("_")[0]
    # token = "6d0e48500c618bb1028112432351b6d4"
    sign = hashlib.md5()
    datas = token + '&' + t + '&' + appkey + '&' + data
    sign.update(datas.encode())
    signs = sign.hexdigest()
    return signs, t

# 解析结果json
def get_itemsArray(response_json):
    start = response_json.find('(')
    itemsArray = (json.loads(response_json[start + 1:-1]))["data"]["itemsArray"]
    return itemsArray

# 目标url
# https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.5&appKey=12574478&t=1556611694443&sign=50cb9beadacdc7006b25feb28f687d7e&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp6&data={"m":"shopitemsearch","vm":"nw","sversion":"4.6","shopId":"58914592","sellerId":"114872995","style":"wf","page":"3","sort":"_coefp","catmap":"","wirelessShopCategoryList":""}

def main():
    # 阿蓝珠宝，总共131件商品，每页返回10个，需要抓取14页
    itemsArray = []
    page = 15
    for i in range(1,page):
    # data = '{"m":"shopitemsearch","vm":"nw","sversion":"4.6","shopId":"58914592","sellerId":"114872995","style":"wf","page":"1","sort":"_coefp","catmap":"","wirelessShopCategoryList":""}'
        print(i)
        data = '{"m":"shopitemsearch","vm":"nw","sversion":"4.6","shopId":"58914592","sellerId":"114872995","style":"wf","page":"'+str(i)+'","sort":"_coefp","catmap":"","wirelessShopCategoryList":""}'
        # 每页都要重新生成 sign
        sign, t = get_sign(data)
        base_url = "https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.5&appKey=12574478&t=" + t + "&sign=" + sign + "&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp6&data="
        request_url = base_url + data
        response_json=session.get(request_url, headers=header).content.decode("utf-8","ignore")
        itemsArray = itemsArray+get_itemsArray(response_json)
        time.sleep(1)
    print(itemsArray)
    return itemsArray

if __name__ == '__main__':
    main()
