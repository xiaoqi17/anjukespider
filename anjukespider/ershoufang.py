# -*- coding: utf-8 -*-
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
item_info = ceshi['ershoufang']



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '}
def page_html( pages):
    try:
        list_view = 'https://guangzhou.anjuke.com/sale/p{}/'.format( str(pages))
        wb_data = requests.get(list_view,headers=headers)
        time.sleep(5)
        if wb_data.status_code == 200:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            for link in soup.select('  div.house-details > div.house-title > a'):
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
            time.sleep(5)
            if wb_data.status_code == 200:
                soup = BeautifulSoup(wb_data.text, 'lxml')
                titles = soup.select(' div.clearfix.title-guarantee > h3')
                residentials = soup.select('div.first-col.detail-col > dl:nth-of-type(1) > dd > a')
                years = soup.select(' div.first-col.detail-col > dl:nth-of-type(3) > dd')
                addrs = soup.select(' div.first-col.detail-col > dl:nth-of-type(2) > dd > p')
                genres = soup.select(' div.first-col.detail-col > dl:nth-of-type(4) > dd ')
                apartments = soup.select('  div.second-col.detail-col > dl:nth-of-type(1) > dd')
                areas = soup.select(' div.second-col.detail-col > dl:nth-of-type(2) > dd')
                orientations = soup.select(' div.second-col.detail-col > dl:nth-of-type(3) > dd')
                floors = soup.select('div.second-col.detail-col > dl:nth-of-type(4) > dd')
                renovations = soup.select('div.third-col.detail-col > dl:nth-of-type(1) > dd')
                units = soup.select('div.third-col.detail-col > dl:nth-of-type(2) > dd')
                down_payments = soup.select('div.third-col.detail-col > dl:nth-of-type(3) > dd')
                monthly_houses = soup.select('div.third-col.detail-col > dl:nth-of-type(4) > dd > span')
                intermediarys = soup.select(' div.img-box > p')
                tels = soup.select(' div.broker-wrap > p')
                for title,residential,year,addr,tel,genre,apartment,area,orientation,floor,renovation,unit,down_payment,monthly_house,intermediary in zip(titles,residentials,years,addrs,tels,genres,apartments,areas,orientations,floors,renovations,units,down_payments,monthly_houses,intermediarys):
                    data ={
                        '楼盘':title.get_text().strip(),
                        '小区':residential.get_text().strip(),
                        '位置':addr.get_text().strip(),
                        '年代':year.get_text().strip(),
                        '类型':genre.get_text().strip(),
                        '房型':apartment.get_text().strip(),
                        '面积':area.get_text().strip(),
                        '朝向':orientation.get_text().strip(),
                        '楼层':floor.get_text().strip(),
                        '装修程度': renovation.get_text().strip(),
                        '单价': unit.get_text().strip(),
                        '首付': down_payment.get_text().strip(),
                        '月供': monthly_house.get_text().strip(),
                        '中介': intermediary.get_text().strip(),
                        '电话': tel.get_text().strip(),
                        '房子链接':url

                    }
                    item_info.insert_one(data)
                    print data

            else:
                print '解析错误'
    except:
        print '解析错误'


