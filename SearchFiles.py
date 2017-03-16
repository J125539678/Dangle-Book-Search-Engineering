#!/usr/bin/env python
# -*- coding:utf8 -*-
import lucene
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, \
    VERSION, initVM, Version, BooleanQuery, BooleanClause


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    allowed_opt = ['kind']
    command_dict = {}
    opt = 'title'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict
                

def run(searcher, analyzer,command):
    while True:
        if command == '':
            return
        command_dict = parseCommand(command)
        querys = BooleanQuery()
        for k, v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                                analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(querys, 300).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        text = []
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            temptext = [doc.get("url"), doc.get('title'), doc.get("imgurl"), doc.get("price"), doc.get("kind")]
            text.append(temptext)
        return text

def search(command):
    STORE_DIR = "index"
    vm_env = initVM()
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    result = run(searcher, analyzer,command)
    searcher.close()
    return result


if __name__ == '__main__':
    STORE_DIR = "index"
    initVM()
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer, '好')
    searcher.close()
