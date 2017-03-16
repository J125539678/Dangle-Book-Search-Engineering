# -*- coding:gbk -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import sys
import chardet
import threading
import Queue
import time

stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    time.sleep(0.5)
    try:
        req = urllib2.Request(page)
        req.add_header('User-Agent', 'fake-client')
        content = urllib2.urlopen(req, timeout = 60).read()
        '''if content.find('img') == '':
            return ""'''
        varLock.acquire()
        varLock.release()
        return content
    except:
        return ""

def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.findAll('a', {'href': re.compile('^http')}):
        url = link.get('href', '')
        p = re.compile('^http://product.dangdang.com/')
        if p.match(url) == None: # �޳���������Ҫ�����ҳ���ӣ��ӿ��ٶ�
            continue
        p_ = re.compile('^http://product.dangdang.com/picture/')
        if p_.match(url) != None:
            continue
        links.append(url)
    return links
       
def add_page_to_folder(page, content):
    global count

    p = re.compile('^http://product.dangdang.com/')
    if p.match(page) == None: # �޳���������Ҫ�����ҳ���ӣ��ӿ��ٶ�
        return
    charset = 'gbk'
    try:
        content = unicode(content, charset, errors='ignore') # ��content���±���
    except:
        print "Failed in encoding."
    index_filename = 'index.txt' 
    folder = 'html' 
    filename = valid_filename(page) 
    filename = filename + '.txt'
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')

    soup = BeautifulSoup(content, "html.parser")
    try:
        page = page + '\n'
        f.write(page) # ��һ����Ϊ��ַ
        print 'downloading page %s' % page

        f.write("title:") # �ڶ�����Ϊ����
        div = soup.find('meta', {'name': 'keywords'})
        title = div.get('content', '')
        if title == "":
            title = soup.find('title', '').contents[0]
        title = title + '\n'
        f.write(title)
        print title

        '''f.write("description:") # ��������Ϊ�������
        div = soup.find('meta', {'name': 'description'})
        description = div.get('content', '') + '\n'
        f.write(description)
        print description'''

        f.write("imgurl:") # ���Ĳ���ΪͼƬ����
        div = soup.find('img', {'id': 'largePic'})
        imgurl = div.get('src', '')
        if imgurl[-4:] != '.jpg':
            imgurl = div.get('wsrc', '')
        imgurl = imgurl + '\n'
        f.write(imgurl)
        print imgurl

        f.write("price:") # ���岿��Ϊ�۸�
        price = "$0.00"
        try:
            try:
                div = soup.find('span', {'class': 'price_d'})
                price = div.contents[0]
            except:
                div = soup.find('i', {'class': 'm_price'})
                price = div.contents[0]

        except:
            pass
        f.write(price)
        print price
        
        count += 1
        print count
        
    except:
        print "Failed in getting content."
    
    f.close()
    
def crawl(): 
    while True and count < max_page:
        try:
            page = q.get()
            if page not in crawled:
                crawled.append(page)
                content = get_page(page)
                if content == "":
                    crawled.append(page)
                    continue
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                for link in outlinks:
                    q.put(link)
                if varLock.acquire():
                    varLock.release()
                q.task_done()
        except:
            pass
    while(q.qsize()>0):
        try:
            q.task_done()
        except:
            pass

start = time.clock()
NUM = 200
count = 0
max_page = 10000
crawled = []
varLock = threading.Lock()
q = Queue.Queue()
q.put('http://book.dangdang.com/01.30.htm')
for i in range(NUM):
    t = threading.Thread(target = crawl)
    t.setDaemon(True)
    t.start()
q.join()
end = time.clock()
time.sleep(1.5)
print end-start
