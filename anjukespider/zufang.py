# -*- coding: utf-8 -*-
import json
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
item_info = ceshi['zufang']
m_item_info =  ceshi['m_zufang']


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '}
def page_html(pages):
    try:
        list_view = 'https://gz.zu.anjuke.com/fangyuan/p{}/'.format( str(pages))
        wb_data = requests.get(list_view,headers=headers)
        time.sleep(5)
        if wb_data.status_code == 200:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            for link in soup.select(' div.zu-info > h3 > a'):
                url = link.get('href')
                print url
                yield url
        else:
            print '%s链接解析错误'%list_view
    except:
        print '链接解析错误'

def text_html(url):
    try:
        if item_info.find_one({'房子链接': url}):
            print '%s爬过'%url
        else:
            wb_data = requests.get(url,headers=headers)
            time.sleep(5)
            if wb_data.status_code == 200:
                text = re.sub('<a class="loan-link" href="https://gz.fang.anjuke.com/jinrong/" _soj="zffy" target="_blank">.*?</a>','',wb_data.text)
                soup = BeautifulSoup(text, 'lxml')
                titles = soup.select('  div.tit.cf > h3')
                residentials = soup.select(' div.litem.fl > dl:nth-of-type(5) > dd > a')
                zujins = soup.select('  div.litem.fl > dl:nth-of-type(1) > dd')
                yafus = soup.select('  div.litem.fl > dl:nth-of-type(2) > dd')
                fangxings = soup.select(' div.litem.fl > dl:nth-of-type(3) > dd ')
                zlfss = soup.select(' div.litem.fl > dl:nth-of-type(4) > dd')
                addrs = soup.select(' div.litem.fl > dl:nth-of-type(6) > dd')
                zhuangxius = soup.select('   div.ritem.fr > dl:nth-of-type(2) > dd')
                mianjis = soup.select('  div.ritem.fr > dl:nth-of-type(3) > dd')
                chaoxiangs = soup.select(' div.ritem.fr > dl:nth-of-type(4) > dd')
                louchengs = soup.select(' div.ritem.fr > dl:nth-of-type(5) > dd')
                leixings = soup.select(' div.ritem.fr > dl:nth-of-type(6) > dd')
                configures = soup.select('#proLinks > p')
                intermediarys = soup.select(' div.broker_rig_info > h2')
                tels = soup.select('  div.broker_infor > p')
                for title,residential,zujin,yafu,fangxing,zlfs,addr,zhuangxiu,mianji,chaoxiang,loucheng,leixing,configure,intermediary,tel in zip(titles,residentials,zujins,yafus,fangxings,zlfss,addrs,zhuangxius,mianjis,chaoxiangs,louchengs,leixings,configures,intermediarys,tels):
                    data ={
                            '楼盘':title.get_text().strip(),
                            '小区':residential.get_text().strip(),
                            '租金':zujin.get_text().strip(),
                            '租金押付':yafu.get_text().strip(),
                            '房型':fangxing.get_text().strip(),
                            '租赁方式':zlfs.get_text().strip(),
                            '位置':addr.get_text().strip(),
                            '装修':zhuangxiu.get_text().strip(),
                            '面积':mianji.get_text().strip(),
                            '朝向': chaoxiang.get_text().strip(),
                            '楼层': loucheng.get_text().strip(),
                            '配置': configure.get_text().strip(),
                            '中介': intermediary.get_text().strip(),
                            '电话': tel.get_text().strip(),
                            '房子链接':url

                        }
                    item_info.insert_one(data)
                    print data

            else:
                pass
    except:
        print '%s解析错误'%url

