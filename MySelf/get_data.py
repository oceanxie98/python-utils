# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import json

url_detial = []  # 各区域url
filename_s = []  # 文件姓名


# 获取页面数据
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    return html.text


# 分析单个页面
def parse_one_page(html):
    n=0
    ava=0
    title = []
    datas = []  # 单个页面的数据
    baseinfo = []  # 基础信息
    address = []  # 地址
    message_s = []  # 状态
    sum = []  # 房价
    unit = []  # 单价
    time = []

    html_etree = etree.HTML(html)
    # 标题
    title = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//span[@class="title_des"]/text()')
    # 基础信息
    baseinfo_1 = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="baseinfo"][1]/span[1]/text()')
    baseinfo_2 = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="baseinfo"][1]/span[2]/text()')
    baseinfo_3 = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="baseinfo"][1]/span[3]/text()')
    for (baseinfo1, baseinfo2, baseinfo3) in zip(baseinfo_1, baseinfo_2, baseinfo_3): baseinfo.append(
        baseinfo1 + " " + baseinfo2 + baseinfo3)
    # 地址
    address_1 = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="baseinfo"][2]/span[1]/text()')
    address_2 = html_etree.xpath(
        '//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="baseinfo"][2]/span[2]/text()')
    for (address1, address2) in zip(address_1, address_2):
        address.append(address1 + address2)
    # 状态
    message_ = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="list-info"]//p[@class="tag-wrap"]')
    for message in message_:
        message_1 = message.xpath('normalize-space(string(.))').strip()
        message_s.append(message_1)
    # 价格
    sum_1 = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="price"]//b/text()')#int型价格
    sum_2 = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="price"]//span/text()')
    for (sum1, sum2) in zip(sum_1, sum_2):  # 拼接价格
        sum.append(sum1 + sum2)
    # 单价
    unit_1 = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="price"]//p[2]/span/text()')
    unit_2 = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="price"]//p[2]/text()')
    # for item in unit_2:
    #     unit_2_1=item.xpath('string(.)').strip()
    for (unit1, unit2) in zip(unit_1, unit_2):
        unit.append(unit1 + "元/㎡/天")
    # 发布时间
    time = html_etree.xpath('//ul[@class="house-list-wrap"]/li//div[@class="time"]/text()')
    for (title_byte, baseinfo_byte, address_byte, message_s_byte, sum_byte, unit_byte, time_byte) in zip(title,baseinfo,address,message_s,sum,unit,time):
        yield {
            'title': title_byte,
            'address': address_byte,
            'price': sum_byte,
            'unit': unit_byte
        }
        # data = {
        #     'title': title_byte,
        #     'address': address_byte,
        #     'price': sum_byte,
        #     'unit': unit_byte
        # }


# 写入文件
def write_to_file(filename, item):
    with open(filename + '.json', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(item, indent=2, ensure_ascii=False) + ",")


# 获取各区域url及区域名
def get_detial_url(html):
    url_etree = etree.HTML(html)
    urls_list= url_etree.xpath('//dl[@class="secitem"][1]/dd/a[@name="b_link"]/@href')
    for url1 in urls_list:
        url_detial.append("http://cd.58.com" + url1)
    for filename1 in urls_list:
        filename2=filename1.split('/shangpucz/')[0].lstrip('/')
        filename_s.append(filename2)


url_total="http://cd.58.com/shangpucz/"
html_total=get_one_page(url_total)
get_detial_url(html_total)
for (url,filename) in zip(url_detial,filename_s):
    for i in range(1,70):
        url_page=url+"pn"+str(i)
        print(url_page)
        html=get_one_page(url_page)
        parse_one_page(html)
        for item in parse_one_page(html):
            write_to_file(filename,item)
        # print("page" + str(i))
    time.sleep(1)

