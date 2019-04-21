#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import json
import requests

"""
589215495706
570682278295
586919663297
571024818873
581663957867
581847174467
550322812402
586891669550
"""
def getHtmlJson(id):
    result_arr = []
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
    session = requests.Session()
    url = r'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=1535083295045' \
          r'&sign=ef22a6dc765bd6ce86d36e2ba9a6cc33&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017' \
          r'%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%7B%22itemNumId%22%3A%22' + str(
        id) + r'%22%7D '
    # print(url)
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['data']

    #----------------------------------
    # 商品名
    title = datas['item']['title']
    # 商品现有价格和库存
    skuCore = json.loads(datas['apiStack'][0]['value'])['skuCore']['sku2info']

    for skuId in skuCore.keys():
        if skuId != '0':
            result_dict = {}
            price = skuCore[skuId]['price']['priceText']
            quantity = skuCore[skuId]['quantity']
            result_dict["id"] = id
            result_dict["skuId"] = skuId
            result_dict["名字"] = title
            result_dict["价格"] = price
            result_dict["库存"] = quantity

            try:
                skus = datas['skuBase']['skus']
                props = datas['skuBase']['props']
                for item in skus:
                    if skuId==item["skuId"]:
                        propPath = item["propPath"].split(";")
                        size_id = propPath[0].split(":")
                        for itm in props:
                            if size_id[0]==itm["pid"]:
                                for it in itm["values"]:
                                    if str(size_id[1])==it["vid"]:
                                        result_dict["规格"] = it["name"]
                                        result_dict["分类"] = ""
                                        if len(propPath) == 1:
                                            result_dict["image"] = "https:" + it["image"]
                            if len(propPath) >= 2:
                                colour_id = propPath[-1].split(":")
                                if colour_id[0]==itm["pid"]:
                                    for it in itm["values"]:
                                        if colour_id[1] == it["vid"]:
                                            result_dict["分类"] = it["name"]
                                            result_dict["image"] = "https:" + it["image"]
            except Exception as e:
                print(e)
                result_dict["规格"] = ""
                result_dict["分类"] = ""
                result_dict["image"] = ""
            result_arr.append(result_dict)
        elif skuId == '0':
            result_dict = {}
            price = skuCore[skuId]['price']['priceText']
            quantity = skuCore[skuId]['quantity']
            result_dict["id"] = id
            result_dict["skuId"] = skuId
            result_dict["名字"] = title
            result_dict["价格"] = price
            result_dict["库存"] = quantity
            result_dict["规格"]=""
            result_dict["分类"]=""
            try:
                image = datas['item']['images'][0]
                result_dict["image"] = image
            except Exception as e:
                print(e)
                result_dict["name"] = ""
                result_dict["image"] = ""
                result_dict["规格"] = ""
                result_dict["分类"] = ""
            result_arr.append(result_dict)
    return result_arr



from io import BytesIO
import xlsxwriter
import time
def create_workbook():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    # 设置Sheet的名字为download
    worksheet = workbook.add_worksheet('download')
    # 列首
    title = ["图片","id","skuId","名字","规格","分类","价格","库存"]
    worksheet.write_row('A1', title)
    dictList = []
    file = open("id","r",encoding="utf-8")
    for i_id in file.read().strip().split("\n"):
        dictList += getHtmlJson(i_id)
    for i in range(len(dictList)):
        row = [dictList[i]["image"],dictList[i]["id"],dictList[i]["skuId"],dictList[i]["名字"],dictList[i]["规格"],dictList[i]["分类"],dictList[i]["价格"],dictList[i]["库存"]]
        worksheet.write_row('A' + str(i + 2), row)
        # # 缓存图片
        # image_data = BytesIO(ru.urlopen(dictList[i]["image"]).read())
        # # 插入图片
        # worksheet.insert_image('B' + str(i + 1), dictList[i]["image"], {'image_data': image_data})
        i += 1
    workbook.close()
    response = make_response(output.getvalue())
    output.close()
    return response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    dictList = []
    if request.method == 'GET':
        return render_template("index.html", dictList=dictList)

    elif request.method == 'POST':
        input_id = request.form["goods_id"]
        if len(input_id) > 0:
            with open("id","w",encoding="utf-8") as f:
                f.write(input_id.strip().replace("\n",""))
            f.close()
            for i_id in input_id.strip().split("\n"):
                # dictList.append(getHtmlJson(i_id))
                dictList += getHtmlJson(i_id)
                time.sleep(1)
            return render_template("index.html", dictList=dictList)
        else:
            return render_template("index.html", dictList=dictList)

from flask import make_response
@app.route('/download', methods=['GET'])
def download():

    response = create_workbook()
    response.headers['Content-Type'] = "utf-8"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Content-Disposition"] = "attachment; filename=download"+ str(int(time.time())) +".xlsx"
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(debug=True)