#coding=utf8
# from __future__ import unicode_literals
from common import *
import time
import base64
import pymongo
from lxml import etree
from datetime import datetime, timedelta


def Init():
    # 初始化
    # 连接 mongo 数据库
    mongo_client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s'%(mongo_user,mongo_pwd,mongo_host,mongo_port,mongo_dbname))

    # 切换 mongo 数据库
    mongo_db = mongo_client[mongo_dbname]

    # 获取 mongo 数据库中的集合
    articles = mongo_db['articles']

    return articles

def crawler_cnys(articles):
    # 开始抓取 中华养生网 的医疗资讯
    # 抓取策略：
    # 抓取首页几大类别列出的文章，以标题来判断数据库中是否已存在，如果不存在，抓取文章详情，放入数据库
    url = 'http://www.cnys.com/'
    category_classes = ['icate icate1','icate icate2','icate icate5','icate icate4','icate icate3']
    article_list = []
    # 抓取首页文章信息
    for category_class in category_classes:
        # 获取类别下的文章信息
        items = Parse(url,'//div[@class="ip3"]/div[@class="%s"]//h3 | //div[@class="ip3"]/div[@class="%s"]//li/a[@title]'%(category_class,category_class))
        if items <= 0:
            raise Exception, '首页文章信息获取失败'
        # 获取该类别名
        category_name = items[0].text
        # 将每个类别下的文章依次放入列表
        for item in items[1:]:
            article = {
                'title' : item.attrib['title'].strip(),
                'href' : 'http:' + item.attrib['href'] if item.attrib['href'].find('http')==-1 else item.attrib['href'],
                'category' : category_name,
            }
            article_list.append(article)

    # 抓取文章详情，放入数据库
    for idx, article in enumerate(article_list):
        res = articles.find_one({'title':article['title']})
        # 数据库中已存在，不放入数据库
        if res != None:
            printx('[%d] 文章《%s》已存在数据库！'%(idx+1, article['title'].encode('utf8')))
            continue
        # 数据库中还没有，抓取文章详情，并放入数据库
        items = Parse(article['href'],'//div[@class="reads"]')
        if items <= 0:
            raise Exception, '文章详情获取失败'
        article['content'] = etree.tostring(items[0]).strip()
        article['read'] = 0
        article['upvote'] = 0
        article['publisher'] = '中华养生网'
        article['publisher_src'] = 'http://www.cnys.com/'
        article['pubdate'] = datetime.now()
        img = items[0].xpath('//div[@class="reads"]//img[1]')               # 取出第一个img元素的src
        img = '' if len(img)==0 else img[0].attrib['src']                   # 取不到就赋空串
        article['img'] = img                                                
        intro = items[0].xpath('//div[@class="reads"]/p[1]')[0].text             # 取出第一个p元素的内容
        intro = article['title'] if intro == None else intro.strip()   # 取不到就用标题代替
        article['intro'] = intro     
        # 插入数据库
        printx('[%d] 文章《%s》正在放入数据库……'%(idx+1, article['title'].encode('utf8')))
        articles.insert(article)


def main():
    # 主函数

    # 初始化
    printx('正在初始化……')
    articles = Init()

    printx('开始抓取医疗资讯……')
    while True:
        crawler_cnys(articles)

        printx('Sleep %d s...'%watch_interval)

        # 休眠一会
        time.sleep(watch_interval)




if __name__ == '__main__':
    main()
    # while True:
    #     try:
    #         main()
    #     except Exception as e:
    #         printx(str(e))

