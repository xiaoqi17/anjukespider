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
item_info = ceshi['ershoufang']
m_item_info =  ceshi['m_ershoufang']


'''PC端'''
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '}
# def page_html( pages):
#     try:
#         list_view = 'https://guangzhou.anjuke.com/sale/p{}/'.format( str(pages))
#         wb_data = requests.get(list_view,headers=headers)
#         time.sleep(5)
#         if wb_data.status_code == 200:
#             soup = BeautifulSoup(wb_data.text, 'lxml')
#             for link in soup.select('  div.house-details > div.house-title > a'):
#                 url = link.get('href')
#                 print url
#                 yield url
#         else:
#             print '%s链接解析错误'%list_view
#     except:
#         print '链接解析错误'
#
# def text_html(url):
#     try:
#         if item_info.find_one({'url': url}):
#             print '%s爬过'%url
#         else:
#             wb_data = requests.get(url,headers=headers)
#             time.sleep(5)
#             if wb_data.status_code == 200:
#                 soup = BeautifulSoup(wb_data.text, 'lxml')
#                 titles = soup.select(' div.clearfix.title-guarantee > h3')
#                 residentials = soup.select('div.first-col.detail-col > dl:nth-of-type(1) > dd > a')
#                 years = soup.select(' div.first-col.detail-col > dl:nth-of-type(3) > dd')
#                 addrs = soup.select(' div.first-col.detail-col > dl:nth-of-type(2) > dd > p')
#                 genres = soup.select(' div.first-col.detail-col > dl:nth-of-type(4) > dd ')
#                 apartments = soup.select('  div.second-col.detail-col > dl:nth-of-type(1) > dd')
#                 areas = soup.select(' div.second-col.detail-col > dl:nth-of-type(2) > dd')
#                 orientations = soup.select(' div.second-col.detail-col > dl:nth-of-type(3) > dd')
#                 floors = soup.select('div.second-col.detail-col > dl:nth-of-type(4) > dd')
#                 renovations = soup.select('div.third-col.detail-col > dl:nth-of-type(1) > dd')
#                 units = soup.select('div.third-col.detail-col > dl:nth-of-type(2) > dd')
#                 down_payments = soup.select('div.third-col.detail-col > dl:nth-of-type(3) > dd')
#                 monthly_houses = soup.select('div.third-col.detail-col > dl:nth-of-type(4) > dd > span')
#                 intermediarys = soup.select(' div.img-box > p')
#                 tels = soup.select(' div.broker-wrap > p')
#                 for title,residential,year,addr,tel,genre,apartment,area,orientation,floor,renovation,unit,down_payment,monthly_house,intermediary in zip(titles,residentials,years,addrs,tels,genres,apartments,areas,orientations,floors,renovations,units,down_payments,monthly_houses,intermediarys):
#                     data ={
#                         '楼盘':title.get_text().strip(),
#                         '小区':residential.get_text().strip(),
#                         '位置':addr.get_text().strip(),
#                         '年代':year.get_text().strip(),
#                         '类型':genre.get_text().strip(),
#                         '房型':apartment.get_text().strip(),
#                         '面积':area.get_text().strip(),
#                         '朝向':orientation.get_text().strip(),
#                         '楼层':floor.get_text().strip(),
#                         '装修程度': renovation.get_text().strip(),
#                         '单价': unit.get_text().strip(),
#                         '首付': down_payment.get_text().strip(),
#                         '月供': monthly_house.get_text().strip(),
#                         '中介': intermediary.get_text().strip(),
#                         '电话': tel.get_text().strip(),
#                         '房子链接':url
#
#                     }
#                     item_info.insert_one(data)
#                     print data
#
#             else:
#                 print '解析错误'
#     except:
#         print '解析错误'

'''移动端'''
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 '}
def page_html(pages):
    try:
        list_view = 'https://m.anjuke.com/gz/sale/?from=anjuke_home&page={}'.format( str(pages))
        wb_data = requests.get(list_view,headers=headers)
        time.sleep(5)
        if wb_data.status_code == 200:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            for link in soup.select(' #list > div > div > a'):
                url = link.get('href')
                print url
                yield url
        else:
            print '%s链接解析错误'%list_view
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
                text = re.sub('<em>','',text)
                text = re.sub('</em>','',text)
                pattern = re.compile(r'<div class="pro-title" .*?>.*?<span>(.*?)</span>.*?<label>.*?</i><span class="price">(.*?)</span>.*?<label>.*?</i>(.*?)<a .*?>.*?</label>'
                                     '.*?<label>.*?</i>(.*?)</label>.*?<label>.*?</i>(.*?)</label>.*?<label>.*?</i>(.*?)</label>.*?<label>.*?</i>(.*?)</label>.*?<label>.*?</i>(.*?)</label>'
                                     '.*?<label>.*?</i>(.*?)</label>.*?<label class="pro-w"><i>.*?</i>(.*?)<a .*?>.*?</a>.*?</div>',re.S)
                items = pattern.findall(text)
                for item in items:
                    data = {
                        '楼盘': item[0].strip(),
                        '价格': item[1].strip(),
                        '月供': item[2].strip(),
                        '房型': item[3].strip(),
                        '单价':item[4].strip(),
                        '面积':item[5].strip(),
                        '朝向':item[6].strip(),
                        '楼层':item[7].strip(),
                        '年代':item[8].strip(),
                        '小区':item[9].strip(),
                        '房子链接':url
                    }
                    print data
                    m_item_info.insert_one(data)

            else:
                pass
    except:
        print '%s解析错误'%url

