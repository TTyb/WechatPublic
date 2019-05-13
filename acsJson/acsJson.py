#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cna: https://log.mmstat.com/eg.js


"""

import requests
session = requests.session()

def getCna():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://h5.m.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host':'log.mmstat.com'
    }
    url='https://log.mmstat.com/eg.js'
    session.get(url=url,headers=headers)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    print(html_set_cookie)
    return html_set_cookie["cna"]

def get_m_h5_tk():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://h5.m.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host':'h5api.m.taobao.com'
    }
    token_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?jsv=2.5.1&appKey=12574478&t=1557746669646&sign=2af0a315c1ecab69cf7068b75237b0ce&api=mtop.taobao.wireless.home.load&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={"containerId":"main","ext":"{\"h5_platform\":\"h5\",\"h5_ttid\":\"60000@taobao_h5_1.0.0\"}"}'
    cookie = {'isg':'BFZW_P36FvhPRyJco2JJW71apAxY95ox8f4p0MC_QjnUg_YdKIfqQbxSH5lvMJJJ','cna':getCna()}
    r = session.get(token_url, headers=headers,cookies=cookie)
    set_cookie=r.headers['Set-Cookie'].split(';')
    print()
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    print(html_set_cookie)

if __name__ == '__main__':
    getCna()
    get_m_h5_tk()