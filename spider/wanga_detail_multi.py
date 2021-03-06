﻿#-------------------------------------------------------------------------------
# Name:        WangaDetail
# Purpose:     Wanga游戏抓取 multi thread
#
# Author:      winxos
# Created:     2/12/2011
# Modified:    19/10/2012
# Copyright:   (c) winxos 2011-2012
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,re,threading,os,sys
from sqlite3 import *
from time import clock
from Queue import Queue

DB_NAME='wanga_detail.db'
SUB_PAGE="http://wanga.me/%s"

#游戏数据结构
class gameinfo:
    def __init__(self):
        self.name=''#名称
        self.id=0#页面ID
        self.type=''#类型
        self.tag=''#标签
        self.detail=''#详情
        self.src=''
    def ToString(self):
        return str(self.id)+self.name+self.type+self.src+self.tag+self.detail


def GetGameInfo(gameid):
    uri=SUB_PAGE%gameid
    try:
        page=urllib2.urlopen(uri,timeout=3) #超时
        data=page.read()
        page.close()
    except Exception,e: #捕捉访问异常，一般为timeout，信息在e中
        return None
    
    g=gameinfo()
    g.id=int(gameid)
    data=unicode(data,'utf-8')#网页编码为utf-8

    p1=re.compile('entry-title">([^<]*)') #得到名称
    m1=p1.search(data)
    if m1!=None:
        g.name=m1.group(1)
    p2=re.compile('embed src="([^"]*)"') #得到地址
    m2=p2.search(data)
    if m2==None:#页面有的使用内嵌框架的
        p2=re.compile('iframe src="([^"]*)"')
        m2=p2.search(data)
        #print gameid,",iframe"
    if m2!=None:
        g.src=m2.group(1) #地址
        #中文介绍
        p5=re.compile('description" content="([^"]+)') #网站有调整，介绍抓取变简单了
        m5=p5.search(data)
        if m5!=None:
            g.detail=m5.group(1)
        else:
            print gameid,"no content"
    else:#没有插入游戏的情况
        print gameid,"no src"
        g.src=""

    p3=re.compile('category tag">([^<]*)<') #得到type
    m3=p3.search(data)
    if m3!=None:
        g.type=m3.group(1)

    p4=re.compile('rel="tag">([^<]*)<')#得到tag
    m4=p4.findall(data)
    g.tag=' '.join(m4)
    return g
#文件线程类
class FileGetter(threading.Thread):
    def __init__(self, gameid):
        self.id = gameid
        self.result = None
        threading.Thread.__init__(self)#初始化，必须

    def get_result(self):
        return self.result

    def run(self):
        try:
            self.result = GetGameInfo(self.id)
            while self.result==None:
                self.result = GetGameInfo(self.id)
        except Exception,e:
            print "!%s: %s" % (self.id,e)
#多线程文件下载，线程池
def get_files(files):
    finished=[] #用于存放结果
    def producer(q, files): #用于产生线程
        for gameid in files:
            thread = FileGetter(gameid)
            thread.start()
            q.put(thread, True)
    def consumer(q, total_files): #线程调用
        while len(finished)<total_files: #线程未完成
            thread = q.get(True)
            thread.join()
            finished.append(thread.get_result()) #完成任务结果加入列表
            if len(finished)%50==0:print len(finished)
    q = Queue(5)#线程池大小
    prod= threading.Thread(target=producer, args=(q, files)) #线程使用
    cons = threading.Thread(target=consumer, args=(q, len(files)))
    prod.start()
    cons.start()
    prod.join()
    cons.join() #等待完成
    return finished

#建立详细游戏资料库，包含id，名字，标签，源地址，说明等
def CreateDetailLib():
    ifile=open("wanga_id.txt").read()
    mu=list(set(ifile.split()))#去除重复元素
    start=clock()#计时
    ans=get_files(mu)
    print "total time collapsed:%f"%(clock()-start)
    if os.path.isfile(DB_NAME):#已经建立数据库
        conn=connect(DB_NAME)
        curs=conn.cursor()
    else:
        conn=connect(DB_NAME)
        curs=conn.cursor()
        curs.execute('create table gamelist(id integer primary key, name text, \
                        type text, src text, tag text, detail text)')
    for a in ans:
        try:
            if a.src!="":
                st='insert into gamelist values(%d,"%s","%s","%s","%s","%s")'%\
                    (a.id,a.name,a.type,a.src,a.tag,a.detail)
                st=' '.join(st.split())#去除空白符和换行符
                curs.execute(st)
        except Exception,e:
            print e
    conn.commit()
    conn.close()
if __name__ == '__main__':
    CreateDetailLib()

