#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests


def get_Cookie2_t_token(shop_name,shop_id,session):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'login.taobao.com'
    }
    url = "https://login.taobao.com/jump?target=https://"+str(shop_name)+".m.tmall.com/?tbpm=1&ajson=1&parentCatId=0&shop_id=" + shop_id
    session.get(url=url, headers=headers)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    return html_set_cookie

def get_m_h5_tk(shop_name,shop_id,session):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://'+str(shop_name)+'.m.tmall.com/?ajson=1&parentCatId=0&shop_id=' + shop_id,
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'h5api.m.tmall.com'
    }
    _m_h5_tk_url = 'https://h5api.m.tmall.com/h5/mtop.shop.render.getpageview/1.0/?jsv=2.4.8&appKey=12574478&t=1557914653186&sign=660afbc5af93a17f28721a1be5d7110c&api=mtop.shop.render.getpageview&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={}'
    cookie = {'isg': 'BC4ucq8U_sXxaQohN_Z3oCUNfITwL_IpGTZBSFj3mjHsO86VwL9COdQ992Fy-OpB',
              't': get_Cookie2_t_token(shop_name,shop_id,session)["t"], '_tb_token_': get_Cookie2_t_token(shop_name,shop_id,session)["_tb_token_"],
              "cookie2": get_Cookie2_t_token(shop_name,shop_id,session)["cookie2"]}
    session.get(_m_h5_tk_url, headers=headers, cookies=cookie)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    enc_url = "https://h5api.m.tmall.com/h5/mtop.taobao.geb.enhenced.itemlist.get/2.0/?jsv=2.4.8&appKey=12574478&t=1557972233869&sign=02d52c49694c3d90d08ff9f4afaa8a67&api=mtop.taobao.geb.enhenced.itemlist.get&v=2.0&type=originaljson&timeout=3000&AntiCreep=true&dataType=json&H5Request=true&data={\"ownerId\":\"\",\"itemIds\":\"\",\"pageSize\":1,\"isAuto\":false}"
    session.get(enc_url, headers=headers, cookies=cookie)
    enc_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    html_set_cookie["enc"]=enc_set_cookie["enc"]
    return html_set_cookie


# 获取所有的cookie
def getAllCookies(shop_name,shop_id,session):
    Cookie2_t_token = get_Cookie2_t_token(shop_name,shop_id,session)
    m_h5_tk = get_m_h5_tk(shop_name,shop_id,session)

    cookie = {'isg': 'BLCw7c-nmEVcK0RBYGON1IbJgn4C-ZRDqxgPAqoBfIveZVAPUglk0wYTuaugbkwb',
              'enc': m_h5_tk["enc"],
              't': Cookie2_t_token["t"], '_tb_token_': Cookie2_t_token["_tb_token_"],
              "cookie2": Cookie2_t_token["cookie2"], '_m_h5_tk_enc': m_h5_tk["_m_h5_tk_enc"],
              '_m_h5_tk': m_h5_tk["_m_h5_tk"]}
    return cookie