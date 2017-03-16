# -*- encoding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import lucene
import threading
import time
import urlparse
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""
class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        store = lucene.SimpleFSDirectory(lucene.File(storeDir))
        writer = lucene.IndexWriter(store, analyzer, True,
                                    lucene.IndexWriter.MaxFieldLength.LIMITED)
        writer.setMaxFieldLength(1048576)
        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'optimizing index',
        threading.Thread(target=ticker.run).start()
        writer.optimize()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root2, writer):
        root2 = unicode(root2, "utf8")
        for r, d, f in os.walk(root2):
            for dir in d:
                leibie = dir
                root3 = root2 + '\\' + dir
                for root, dirs, files in os.walk(root3):
                    for filename in files:
                        if len(filename) > 180:continue
                        path = os.path.join(root, filename)
                        f = open(path, 'r')
                        for lines in f:
                            lines = unicode(lines, 'utf-8')
                            start = lines.find(':')
                            kind = lines[0:start]
                            content = lines[start+1::]
                            if kind == 'http':
                                url = 'http:'+content
                            elif kind == 'title':
                                title = content
                            elif kind == 'imgurl':
                                imgurl = content
                            elif kind == 'price':
                                price = content[1::]
                            #print lines[0:start]
                            #print lines
                        #print url, title, imgurl, price
                        f.close()

                        try:
                            doc = lucene.Document()
                            doc.add(lucene.Field("url", url,
                                             lucene.Field.Store.YES,
                                             lucene.Field.Index.NOT_ANALYZED))
                            doc.add(lucene.Field("title", title,
                                             lucene.Field.Store.YES,
                                             lucene.Field.Index.ANALYZED))
                            doc.add(lucene.Field("imgurl", imgurl,
                                             lucene.Field.Store.YES,
                                             lucene.Field.Index.NOT_ANALYZED))
                            doc.add(lucene.Field("price", price,
                                             lucene.Field.Store.YES,
                                             lucene.Field.Index.NOT_ANALYZED))
                            doc.add(lucene.Field("kind", leibie,
                                             lucene.Field.Store.YES,
                                             lucene.Field.Index.ANALYZED))

                            writer.addDocument(doc)
                        except Exception, e:
                            print "Failed in indexDocs:", e


if __name__ == '__main__':
##    if len(sys.argv) < 2:
##        print IndexFiles.__doc__
##        sys.exit(1)

    #crawl(start_page)
    lucene.initVM()
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
##        IndexFiles(sys.argv[1], "index", lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT))
        IndexFiles('HTML', "index", lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT))
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
