import requests
from lxml import etree
import json
import time
import pypinyin
import threading

List = []

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    html=requests.get(url,headers=headers)
    return html.text

def parse_one_page(html):
    date=[]#日期
    weather=[]#天气
    weather_info=[]#天气组合
    air_quality=[]#空气质量
    wind_grade=[]#风级

    html_etree=etree.HTML(html)
    date=html_etree.xpath('//div[starts-with(@class, "table_day")]//h3/b/text()')
    weather=html_etree.xpath('//div[starts-with(@class, "table_day")]//li[2]')
    for weather_res in weather:
        weather_info.append(weather_res.xpath('string(.)').strip())
        #print(weather_info)
    air_quality=html_etree.xpath('//div[starts-with(@class, "table_day")]//li[3]/b/text()')
    wind_grade=html_etree.xpath('//div[starts-with(@class, "table_day")]//li[4]/text()')
    for (date_item,weather_info_item,air_quality_item,wind_grade_item) in zip(date,weather_info,air_quality,wind_grade):
        yield {
            'date':date_item,
            'weather':weather_info_item,
            'air_quality':air_quality_item,
            'wind_grade':wind_grade_item
        }
# 写入文件
def write_to_file(item):
    with open('weather.json', 'w', encoding='utf-8') as fp:#w覆盖写入，a追加写入
        fp.write(json.dumps(item, indent=2, ensure_ascii=False) + ",")

#转换拼音
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

def main():
    url = "http://www.tianqi.com/"+city+"/15"
    html=get_one_page(url)
    print(time.asctime( time.localtime(time.time())))
    for item in parse_one_page(html):
        List.append(item)
        time.sleep(0.5)
        write_to_file(item)
        print('***********************')
        print(item['date'])
        print(item['weather'])
        print(item['air_quality'])
        print(item['wind_grade'])
    global timer
    timer=threading.Timer(60,main)#定时一分钟刷新
    timer.start()





if __name__ == '__main__':
    word=input("请输入你要查询的城市：")
    global city
    city = pinyin(word)
    main()