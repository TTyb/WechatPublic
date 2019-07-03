import lzstring
import requests
import execjs
import chardet
from urllib.request import urlopen

from urllib.parse import quote,unquote

headers={
'Accept': 'application/json',
'Content-Type': 'application/x-www-form-urlencoded',
'Origin': 'http://shop.m.taobao.com',
'Referer': 'http://shop.m.taobao.com/shop/shop_search.htm?loc=&q=zes%3D&fx=0&lp=0&_input_charset=utf-8&base64=1&olu=&isb=1&sort=default&type=all&jf=0&my=0&paytype=&searchfrom=&pds=tianmao%23h%23shopsearch',
'User-Agent':' Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}

url='http://shop.m.taobao.com/shop/shopsearch/search_page_json.do?isb=&sort=default&type=all&loc=&fx=0&lp=0&jf=0&my=0&paytype=&_input_charset=utf-8&base64=1&q=warP6w%3D%3D&shop_type=&olu='

# url='http://shop.m.taobao.com/shop/shopsearch/search_page_json.do?isb=1&sort=default&type=all&loc=&fx=0&lp=0&jf=0&my=0&paytype=&_input_charset=utf-8&base64=1&q=yta7+g==&shop_type=&olu='
# kw='碗'
# url='http://shop.m.taobao.com/shop/shopsearch/search_page_json.do?isb=1&sort=default&type=all&loc=&fx=0&lp=0&jf=0&my=0&paytype=&_input_charset=utf-8&base64=1&q='+quote(kw)+'&shop_type=&olu='
# s='warP6w%3D%3D'
url=str(url)
a=unquote(url)
print(a)

params={
'currentPage': 2,
'pageSize': 24
}
#

#
# #
r=requests.post(url=url,data=params)

print(r.encoding)
print(chardet.detect(r.content))
s=r.text.replace('&quot;','"')
print(s)
# q="&#38518;&#29943;&#25925;&#20107;&#26071;&#33328;&#24215;"
# q='&#25628; &#32034;'
# r=q.replace(';','').split('&#')
# print(r)
# ss=''
# for s in r[1:]:
#     # print(s)
#     ss+=chr(int(s))
# print(ss)
# ic = {"name": "root", "password": "123456"}
# ic = '碗'
# # zes==    warP6w==
# 122  101   115   61   61
# # warP6w==   zes%3D
# x=lzstring.LZString()
# compressed=x.compressToBase64(str(ic))
# print(compressed)
# decompressed=x.decompressFromBase64('zes=')
# print(decompressed)


