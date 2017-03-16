# -*- coding:utf8 -*-
#!/usr/bin/python
import web
import urllib
import lucene
from web import form
import SearchFiles
import programming

urls = (
    '/', 'index',
    '/im', 'index_img',
    '/s/start=(\d+)', 'text',
    '/i/start=(\d+)', 'image',
)
render = web.template.render('templates') # your templates

def func(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    result = SearchFiles.search(command)
    print result
    return result

def func_img(mypic):

    result = programming.search(mypic)
    return result

class index:
    def GET(self):
        return render.index_web()

class index_img:
    def GET(self):
        return render.index_img()

class text:
    result = []
    last_user_data = {}
    def GET(self,start):
        start = int(start)
        user_data = web.input()
        if user_data.get('wd'):   #判断是否需要搜索关键词
            text.last_user_data=user_data
            text.result = func(user_data['wd'])
        elif len(text.last_user_data)>0:
            user_data = text.last_user_data
        else:
            return render.index_web()
        result_len = len(text.result)
        return render.result_web(user_data['wd'], text.result[start:min(start+10,result_len)],result_len, start)

class image:
    def POST(self,start):
        start = int(start)
        user_data = web.input(mypic={})

        if user_data['wd'] != '':
            picname = "".join([a for a in user_data['wd'] if a.isalpha()])+'.jpg'
            picdir = unicode('static/searchpic/'+picname)
            print user_data['wd']
            urllib.urlretrieve(user_data['wd'],picdir)
            result = func_img(picname)
        else:
            print user_data.mypic.filename
            fout = open('static/searchpic/'+user_data.mypic.filename, 'wb')
            fout.write(user_data.mypic.file.read())
            fout.close()
            result = func_img(user_data.mypic.filename)
            picname = user_data.mypic.filename
        result_len = len(result)
        return render.result_img('', picname, result[start:min(start+10,result_len)], result_len, start)

def fileIndexer():
    pass

def imgIndexer():
    pass

if __name__ == "__main__":
    vm_env = lucene.initVM()
    app = web.application(urls, globals())
    app.run()
