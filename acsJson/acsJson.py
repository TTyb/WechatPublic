#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import time
import hashlib
from urllib.parse import quote

session = requests.session()


def getCna():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://h5.m.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'log.mmstat.com'
    }
    url = 'https://log.mmstat.com/eg.js'
    session.get(url=url, headers=headers)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    return html_set_cookie["cna"]


def get_m_h5_tk():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://h5.m.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'h5api.m.taobao.com'
    }
    _m_h5_tk_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?jsv=2.5.1&appKey=12574478&t=1557746669646&sign=2af0a315c1ecab69cf7068b75237b0ce&api=mtop.taobao.wireless.home.load&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={"containerId":"main","ext":"{\"h5_platform\":\"h5\",\"h5_ttid\":\"60000@taobao_h5_1.0.0\"}"}'
    cookie = {'isg': 'BFZW_P36FvhPRyJco2JJW71apAxY95ox8f4p0MC_QjnUg_YdKIfqQbxSH5lvMJJJ', 'cna': getCna()}
    session.get(_m_h5_tk_url, headers=headers, cookies=cookie)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    return html_set_cookie


# https://bbs.125.la/forum.php?mod=viewthread&tid=13766705&highlight=ISG
# 没有破译
def getIsg():
    return "BJaWPGxX1rvRvuIfVNAJbEsj5EyYN9pxMb7pkAD_gnkUwzZdaMcqgfz1W5mK8NKJ"


def getCookie2():
    # https://h5api.m.taobao.com/h5/mtop.user.getusersimple/1.0/?jsv=2.5.1&appKey=12574478&t=1557799048346&sign=483ea07a198f2392e3f1af6eb2756f1d&api=mtop.user.getUserSimple&v=1.0&ecode=1&sessionOption=AutoLoginOnly&jsonpIncPrefix=liblogin&type=jsonp&dataType=jsonp&callback=mtopjsonpliblogin3&data={}
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://h5.m.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'h5api.m.taobao.com'
    }
    cookie2_url = 'https://h5api.m.taobao.com/h5/mtop.user.getusersimple/1.0/?jsv=2.5.1&appKey=12574478&t=1557799048346&sign=483ea07a198f2392e3f1af6eb2756f1d&api=mtop.user.getUserSimple&v=1.0&ecode=1&sessionOption=AutoLoginOnly&jsonpIncPrefix=liblogin&type=jsonp&dataType=jsonp&callback=mtopjsonpliblogin3&data={}'
    cookie = get_m_h5_tk()
    cookie["isg"] = getIsg()
    r = session.get(cookie2_url, headers=headers, cookies=cookie)
    set_cookies = re.split(";|,", r.headers['Set-Cookie'])
    cookie2 = {}
    for item in set_cookies:
        try:
            key = item.strip().split("=")[0]
            value = item.strip().split("=")[1]
            cookie2[key] = value
        except:
            pass
    for key in ["t", "cookie2", "_tb_token_"]:
        if key in cookie2.keys():
            cookie[key] = cookie2[key]
    return cookie


# 没有破译
# l要保持实时更新，不然会返回：非法获取
# mtopjsonp1({"api":"mtop.taobao.wsearch.h5search","data":{},"ret":["FAIL_SYS_ILLEGAL_ACCESS::非法请求"],"v":"1.0"})
def getL():
    return "bBaRc8HVvV3v2fOaBOCahurza77OSIOYYuPzaNbMi_5al6L12RbOldyJUFp6V_CR_s8B4oIS68J9-etli"


def getAllCookies():
    cookie2 = getCookie2()
    cookie2["l"] = getL()
    return cookie2


# 获取秘钥
def get_sign(data):
    t = str(int(time.time() * 1000))
    # t = "1557826901783"
    appkey = "12574478"
    set_cookie = get_m_h5_tk()
    token = set_cookie["_m_h5_tk"].split("_")[0]
    # token = "5b81beddc56e6bc19d9dc718e2fd2d47"
    sign = hashlib.md5()
    datas = token + '&' + t + '&' + appkey + '&' + data
    sign.update(datas.encode())
    signs = sign.hexdigest()
    return signs, t


def getJson(page, keyword):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'referer': 'https://s.m.taobao.com/h5?search-btn=&event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'acs.m.taobao.com'
    }
    cookies = getAllCookies()
    data = '{"event_submit_do_new_search_auction":"1","_input_charset":"utf-8","topSearch":"1","atype":"b","searchfrom":"1","action":"home:redirect_app_action","from":"1","q":"python","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"44","wlsort":"44","page":1}'
    signs, t = get_sign(data)
    base_url = 'https://acs.m.taobao.com/h5/mtop.taobao.wsearch.h5search/1.0/?jsv=2.3.16&appKey=12574478&t=' + t + '&sign=' + signs + '&api=mtop.taobao.wsearch.h5search&v=1.0&H5Request=true&ecode=1&AntiCreep=true&AntiFlool=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=' + quote(data)
    r = session.get(url=base_url, headers=headers, cookies=cookies)
    print(r.text)


if __name__ == '__main__':
    page = 1
    keyword = "python"
    getJson(page, keyword)
