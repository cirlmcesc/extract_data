#!/usr/bin/python2
#This Python file uses the following encoding: utf-8

import Queue
import BeautifulSoup
import requests
import urllib
import thread
import threading
import math
import random
import re
import datetime
import os, time
import sys

import config
import lib
import mysql

def main():
    mysqldb = mysql.proMysql(config.config['mysql_config']) #get mysql instance

    hidtrs = "6D26588A1B71AA977C6C5D0510A307CDB5D119D074727A06A03BFD2E40B5329A9DA38EB8D9DDC70B" #未知意义的参数...

    cluster_list = getClustersAndExtractData()

    mysqldb.insert(table = 'legal_cluster', dictionary = cluster_list) #将索引数据写入数据库, 写入一次即可

    # singleSearchPageTest(u'825', 2, u'660', hidtrs) #手动输入数据

    for cluster in cluster_list: #遍历省份
        cluster['count'] = int(cluster['count'])

        max_page = cluster['count'] / 40 if cluster['count'] % 40 == 0 else cluster['count'] / 40 + 1 #计算最大页数

        print u"%s, 共 %s 条数据, 共 %s 页 ..." % (cluster['province'], cluster['count'], str(max_page))

        for page in range(0, max_page): #遍历所有页
            print u"处理第 %s 页 ..." % (page + 1)

            api_content = getSearchResault(cluster['code'], page, max_page, hidtrs) #获得单页内容

            data, hidtrs = processSingleSearchPageResualt(cluster['code'], api_content) #获得一页数据和密文

            mysqldb.insert(table = 'legal_data', dictionary = data) #将单页数据写入数据库

    return

def singleSearchPageTest(cluster_code, page, page_count, hidtrs): #单页异常调试
    print u"尝试抓取页面 ... cluster_id: %s, 第 %s 页" % (cluster_code, page)
    
    api_content = getSearchResault(cluster_code, page, page_count, hidtrs) #获得单页内容

    print u"尝试分析数据 ..."

    data, hidtrs = processSingleSearchPageResualt(cluster_code, api_content) #获得一页数据和密文

    print data, hidtrs

    exit()

def getClustersAndExtractData(): #获取所有省份数据索引并提取数据
    print u"抓取索引数据 ..."

    resault = requests.post("http://www.pkulaw.cn/doCluster.ashx", headers = {
        'User-Agent': random.choice(config.config['ualist'])
    }, data = {
        "Db": "lar",
        "fieldsname": urllib.quote(urllib.quote("效力级别|发布部门|时效性|类别")),
        "valuepath": urllib.quote("0/XO08|1|2|3"),
        "valuepath_expandstatus": urllib.quote("true|true|true|true"),
        "leafall": urllib.quote("1|0|0|0"),
    })

    data = []

    soup = BeautifulSoup.BeautifulSoup(resault.text).findAll('table')[3].findAll('div') #获得所有数据所在的div

    print u"分析索引数据 ..."

    for data_div in soup: #循环数据块
        clusters = data_div.findAll("a")

        for cluster_tag_a in clusters: #循环所有cluster的a标签
            data.append(extractClusterDataFromTagA(cluster_tag_a))

    return data

def extractClusterDataFromTagA(tag_a): #从A标签中提取cluster数据
    string_part = tag_a.getText() #文字及总数部分

    code_part = tag_a['href'] #cluster的id部分

    code_patr_string_index = code_part.find("/") + 1 #/所在的在的位置+1就是代码的位置

    instance = {}

    instance['province'] = string_part[0 : string_part.find("(")]

    instance['count'] = string_part[string_part.find("(") + 1 : string_part.rfind(")")]

    instance['code'] = code_part[code_patr_string_index : code_patr_string_index + 3]

    return instance

def getSearchResault(cluster_code, page, page_count, hidtrs): #获得单页结果    
    resault = requests.post("http://www.pkulaw.cn/doSearch.ashx", headers = {
        'User-Agent': random.choice(config.config['ualist'])
    }, data = {
        "range": "name",
        "Search_Mode": "accurate",
        "check_hide_xljb": 1,
        "Db": "lar",
        "check_gaojijs": 1,
        "orderby": urllib.quote(urllib.quote("发布日期")).lower(),
        "hidtrsWhere": hidtrs,
        "clusterwhere": enscriptClusterWhereString(cluster_code),
        "aim_page": page,
        "page_count": page_count,
        "clust_db": "lar",
        "menu_item": "law",
        "time": random.random()
    })

    return resault.text

def enscriptClusterWhereString(cluster_code): #加密查询条件字符串
    clusterwhere = (u"效力级别=XO08 and 发布部门=" + cluster_code) #XO08 效力级别=地方政府规章

    return urllib.quote(urllib.quote(clusterwhere.encode('utf-8'))).lower(),

def processSingleSearchPageResualt(cluster_code, api_content): #处理单页数据
    soup, hidtrs = extractDataFromSingleSearchPageResualt(api_content)

    data = []

    index = 0

    while index < 120: #每三个tr为一条数据, 一页40条数据
        try:
            infos = soup[index + 1].find("span").findAll("span")
        except AttributeError:
            break;

        abstracts = getLegalAbstractAndextractData(soup[index + 1])

        instance = {
            'title': soup[index].find("a").getText(), #标题
            'cluster_id': cluster_code, #发布部门ID
            'issued_number': '', #发文字号
            'timeliness': '', #时效性
            'release_date': '', #发布日期
            'implementation_date': '', #实施日期
            'publishing_department': abstracts[0].getText(), #发布部门
            'potency_level': abstracts[1].getText(), #效力级别
            'legal_category': abstracts[2].getText(), #法规类别
        }

        for content in infos:
            string = content.getText().replace("&nbsp;", "") #去除空格符

            if u'号' in string:
                instance['issued_number'] = string
            elif u'效' in string:
                instance['timeliness'] = string
            elif u'发布' in string:
                instance['release_date'] = string
            elif u'实施' in string:
                instance['implementation_date'] = string

        data.append(instance)

        index += 3 #每三个tr为一条数据

    return data, hidtrs

def extractDataFromSingleSearchPageResualt(api_content): #提取数据部分
    soup = BeautifulSoup.BeautifulSoup(api_content)

    hidtrs = soup.find(id = "hidtrsWhere")
    
    soup.find("tr").decompose() #删除标题tr
    
    soup = soup.find("tr").find("td").find("table").find("table") #找到数据所在的tabl

    soup.find("tr").decompose() #删除分页tr
    
    soup.find("tr").decompose() #删除分页tr

    return soup.findAll("tr", limit = 120), hidtrs['value']

def getLegalAbstractAndextractData(tr_content): #获得信息内容并提取数据
    try:
        param = tr_content.find("a")['id'].split("_") 
    except KeyError: #会出现有中英文两个选项, 选择中文
        param = tr_content.findAll("a")[1]['id'].split("_")

    for key in range(0, 4):
        param[key] = str(param[key])

    try:
        resault = requests.get("http://www.pkulaw.cn/get_abstract.ashx?", headers = {
            'User-Agent': random.choice(config.config['ualist'])
        }, params = {
            "Db": param[1],
            "Gid": param[2],
            "infotype": param[3],
            "rand": param[4],
        })

        soup = BeautifulSoup.BeautifulSoup(resault.text)

        soup = soup.find('table').findAll("a", limit = 3)
    except requests.exceptions.ReadTimeout: #请求超时则休眠一分钟后重新尝试
        time.sleep(60)

        return getLegalAbstractAndextractData(tr_content)
    except AttributeError: #尝试重新获得数据
        return getLegalAbstractAndextractData(tr_content) 

    return soup

if __name__ == '__main__':
    main() #execute
