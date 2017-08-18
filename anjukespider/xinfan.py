# -*- coding: utf-8 -*-
import re
import requests
import sys
from bs4 import BeautifulSoup
import time
import pymongo
reload(sys)
sys.setdefaultencoding('utf-8')


client = pymongo.MongoClient('localhost', 27017)
ceshi = client['anjukespier']
url_list = ceshi['url_list']
item_info = ceshi['xinfan']
m_item_info = ceshi['m_xinfan']

'''PC端'''
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '}
# def page_html(pages):
#     try:
#         list_view = 'https://gz.fang.anjuke.com/loupan/all/p{}/'.format( str(pages))
#         wb_data = requests.get(list_view,headers=headers)
#         time.sleep(2)
#         if wb_data.status_code == 200:
#             soup = BeautifulSoup(wb_data.text, 'lxml')
#             for link in soup.select(' div.lp-name > h3 > a'):
#                 url = link.get('href')
#                 url_list.insert_one({'url': url})
#                 print url
#                 yield url
#         else:
#             print '%s链接解析错误'%list_view
#     except:
#         print '链接解析错误'
#
# def text_html(url):
#     try:
#         if url_list.find_one({'url': url}):
#             print '%s爬过'%url
#         else:
#             wb_data = requests.get(url,headers=headers)
#             time.sleep(1)
#             if wb_data.status_code == 200:
#                 text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-mfth" style="display: none;">.*?</a>','',wb_data.text)
#                 text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-ljth" style="display: none;">.*?</a>','',text)
#                 text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-yyhd" style="display: none;">.*?</a>', '',text)
#                 soup = BeautifulSoup(text, 'lxml')
#                 titles = soup.select(' h1')
#                 prices = soup.select('dd.price > p > em')
#                 houses = soup.select('dd.ajust > div')
#                 addrs = soup.select(' dd > span[class="lpAddr-text"]')
#                 tels = soup.select('#phone_show_soj > p ')
#                 openings = soup.select(' ul.info-left > li:nth-of-type(1) > span')
#                 buildings = soup.select(' ul.info-left > li:nth-of-type(2) > span')
#                 propertys = soup.select(' ul.info-left > li:nth-of-type(3) > span')
#                 sell_outs = soup.select('div.lp-tit > i')
#                 others = soup.select(' ul.info-right > li:nth-of-type(1) > span')
#                 for title,price,house,addr,tel,opening,building,property,sell_out,other in zip(titles,prices,houses,addrs,tels,openings,buildings,propertys,sell_outs,others):
#                     data ={
#                         '楼盘':title.get_text(),
#                         '期现罄':sell_out.get_text(),
#                         '售价':price.get_text(),
#                         '户型':house.get_text(),
#                         '地址':addr.get_text().strip(),
#                         '电话':tel.get_text().strip(),
#                         '开盘时间':opening.get_text(),
#                         '交房时间':other.get_text(),
#                         '产权':property.get_text(),
#                         '楼盘链接':url
#                     }
#                     item_info.insert_one(data)
#                     print data
#             else:
#                 print '%s链接出现错误'%url
#     except:
#         print '%s链接解析错误'%url

'''移动端'''
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 '}
def page_html(pages):
    try:
        list_view = 'https://m.anjuke.com/gz/loupan/newajax/all/?q=&lat=0&lng=0&page={}'.format( str(pages))
        wb_data = requests.get(list_view,headers=headers)
        time.sleep(5)
        soup = BeautifulSoup(wb_data.text,'lxml')
        for link in soup.select(' body > a'):
            url = link.get('href')
            if url == 'javascript:;':
                pass
            else:
                print url
                yield url


    except:
        print '链接解析错误'

def text_html(url):
    try:
        if m_item_info.find_one({'房子链接': url}):
            print '%s爬过'%url
        else:
            wb_data = requests.get(url,headers=headers)
            time.sleep(5)
            if wb_data.status_code == 200:
                text = wb_data.text
                text = re.sub(r'<span class="lp-price">','',text)
                text = re.sub(r'</span>','',text)
                pattern = re.compile(r'<div class="lpbase">.*?<h1>(.*?)</h1>.*?<em>(.*?)</em>'
                                     '.*? <p class="g-overflow">(.*?)</p>.*?<p class=".*?">(.*?)</p>'
                                     '.*?<p class="g-overflow">(.*?)</p>.*?<p class="g-overflow">(.*?)</p>.*?<p class="g-overflow-third">(.*?)</p>',re.S)

                items = pattern.findall(text)
                for item in items:
                    data={
                        '小区':item[0].strip(),
                        '销售情况': item[1].strip(),
                        '售价': item[2].strip(),
                        '周边均价': item[3].strip(),
                        '开盘': item[4].strip(),
                        '交房': item[5].strip(),
                        '地址': item[6].strip(),
                        '房子链接':url
                    }
                    print data
                    m_item_info.insert_one(data)

            else:
                pass
    except:
        print '%s解析错误'%url

