#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import os
import pandas as pd

from lxml import etree
base_url = 'https://www.cdfinance.com.cn/business.html'
'''https://www.cdfinance.com.cn/business.html?year=2020&month=1#com2'''


year = '2020'
month = '1'

suffix = '?year={}&month={}#com2'.format(year,month)

##response = requests.get(base_url + suffix , timeout= 60)
##
##T = response.text
##
##html = etree.HTML(T)
##
##zaixiankehushu = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[3]/div[2]/div[2]/div[1]/span')


from selenium import webdriver
import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument('--no-sandbox') #让Chrome在root权限运行

chrome_options.add_argument('--disable-dev-shm-usage') #不打开图形界面

chrome_options.add_argument('--headless') #浏览器不提供可视化页面

chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug


outcome = []

def get_data(c):

    year = c[0]
    month = c[1]

    suffix = '?year={}&month={}#com2'.format(year,month)


    #windows
    
##    option = webdriver.ChromeOptions()
##    option.add_argument('headless')
##    driver = webdriver.Chrome(options = option)

    #Linux
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/google/chrome/chromedriver') #Chrome驱动的位置，此学习记录中安装到了Chrome程序根目录，该路径为绝对路径


    driver.get(base_url + suffix )

    time.sleep(3)

    T = driver.page_source

    html = etree.HTML(T)

    fugaishengfen = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[3]/div[2]/div[1]/div[1]/span')[0].text

    fenzhijigoushu = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[3]/div[2]/div[1]/div[2]/span')[0].text
    
    zaidaikehushu = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[3]/div[2]/div[2]/div[1]/span')[0].text

    hujunyue= html.xpath('//*[@id="bod "]/div[4]/div[2]/div[3]/div[2]/div[2]/div[2]/span')[0].text

    daikuanyue = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[6]/div/div[1]/div[2]/h2/span')[0].text

    dangyuejine = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[5]/div/table/tbody/tr[2]/td[2]')[0].text

    dangyuebishu = html.xpath('//*[@id="bod "]/div[4]/div[2]/div[5]/div/table/tbody/tr[2]/td[3]')[0].text

    shijian = '{}年{}月'.format(year,month)

    temp = [shijian,fugaishengfen,fenzhijigoushu,zaidaikehushu,hujunyue,daikuanyue,dangyuejine,dangyuebishu]

    temp = [_.replace(',','') for _ in temp if _ != None]

    #Ori_out.append( temp)
    
    driver.quit()
                        
    return temp

    

def do_something(c):

    try:
        #print(c)
        res = get_data(c)
        #print(c,  res)

        return res
    
    except:

        
        return ['*']*8

c = [(i,j) for i in range(2013,2021) for j in range(1,13) if not( i==2020 and j>6)]




from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp

#array = mp.Array()
#l = mp.Lock()
que = mp.Queue()
pool = ThreadPool()


Ori_out = []
outcome = pool.map(do_something, c)
pool.close()
pool.join()

##for i in range(2013,2016):
##    for j in range(1,13):
##        if not( i==2020 and j>6):
##            print('doing',i,j)
##            #get_data(i,j)
##            try:
##                get_data([i,j])
##            except:
##                print(i,j)
##                outcome.append(['NaN']*7)
    
pd.DataFrame(outcome).to_csv('outcome_zhonghe.csv',encoding= 'gbk',header = None,index =False)

###我修改了一条信息
