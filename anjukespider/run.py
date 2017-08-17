# -*- coding: utf-8 -*-
from multiprocessing import Pool
import zufang
import xinfan
import ershoufang


def xinfan_run(page):
    urls = xinfan.page_html(page)
    for url in urls:
        xinfan.text_html(url)



def ershoufang_run(page):
    urls = ershoufang.page_html(page)
    for url in urls:
        ershoufang.text_html(url)


def zufang_run(page):
    urls = zufang.page_html(page)
    for url in urls:
        zufang.text_html(url)




if __name__ == '__main__':

    pool = Pool()
    pool.map(xinfan_run,[x for x in range(1,61)] )
    pool.map(ershoufang_run,[x for x in range(1,118)])
    pool.map(zufang_run,[x for x in range(1,51)])
    pool.close()
    pool.join()

