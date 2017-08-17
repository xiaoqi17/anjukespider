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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '}
def page_html(pages):
    try:
        list_view = 'https://gz.fang.anjuke.com/loupan/all/p{}/'.format( str(pages))
        wb_data = requests.get(list_view,headers=headers)
        time.sleep(2)
        if wb_data.status_code == 200:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            for link in soup.select(' div.lp-name > h3 > a'):
                url = link.get('href')
                url_list.insert_one({'url': url})
                print url
                yield url
        else:
            print '%s链接解析错误'%list_view
    except:
        print '链接解析错误'

def text_html(url):
    try:
        if url_list.find_one({'url': url}):
            print '%s爬过'%url
        else:
            wb_data = requests.get(url,headers=headers)
            time.sleep(1)
            if wb_data.status_code == 200:
                text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-mfth" style="display: none;">.*?</a>','',wb_data.text)
                text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-ljth" style="display: none;">.*?</a>','',text)
                text = re.sub('<a href="javascript:" class="btn btn-a" id="j-btn-yyhd" style="display: none;">.*?</a>', '',text)
                soup = BeautifulSoup(text, 'lxml')
                titles = soup.select(' h1')
                prices = soup.select('dd.price > p > em')
                houses = soup.select('dd.ajust > div')
                addrs = soup.select(' dd > span[class="lpAddr-text"]')
                tels = soup.select('#phone_show_soj > p ')
                openings = soup.select(' ul.info-left > li:nth-of-type(1) > span')
                buildings = soup.select(' ul.info-left > li:nth-of-type(2) > span')
                propertys = soup.select(' ul.info-left > li:nth-of-type(3) > span')
                sell_outs = soup.select('div.lp-tit > i')
                others = soup.select(' ul.info-right > li:nth-of-type(1) > span')
                for title,price,house,addr,tel,opening,building,property,sell_out,other in zip(titles,prices,houses,addrs,tels,openings,buildings,propertys,sell_outs,others):
                    data ={
                        '楼盘':title.get_text(),
                        '期现罄':sell_out.get_text(),
                        '售价':price.get_text(),
                        '户型':house.get_text(),
                        '地址':addr.get_text().strip(),
                        '电话':tel.get_text().strip(),
                        '开盘时间':opening.get_text(),
                        '交房时间':other.get_text(),
                        '产权':property.get_text(),
                        '楼盘链接':url
                    }
                    item_info.insert_one(data)
                    print data
            else:
                print '%s链接出现错误'%url
    except:
        print '%s链接解析错误'%url
