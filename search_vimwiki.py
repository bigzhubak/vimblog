#!/usr/bin/env python
#encoding=utf-8
'''
vimwiki 中用来查找 wiki 词
'''
import fnmatch
import sys
import os
import time
import re

WIKI_INDEX = 'wiki_index'


class SearchWiki:
    def __init__(self, wiki_name):
        self.wiki_name = wiki_name
        self.mergered_all = {}
        self.mergered_all_sorted = []
        self.wikis_time = {}

    def search(self, path='.'):
        '''找到wiki文件名,并加上时间'''
        #wiki_names = glob.glob('*%s*.wiki' % self.wiki_name)

        pattern = re.compile(r'^\.')
        for wiki in os.listdir(path):
            # 如果是路径，就不要加入
            if os.path.isdir(wiki):
                continue
            if(fnmatch.fnmatchcase(wiki.upper(), ('*%s*' % self.wiki_name).upper())):
                if path != '.':  # 查找子路径,那么 wiki前面要加上路径
                    wiki = path + '/' + wiki
                modify_time = time.localtime(os.path.getmtime(wiki))
                m = pattern.search(wiki)
                if m is None:  # 隐藏的文件不要参与查找
                    wiki = os.path.basename(wiki)
                    wiki = wiki.rsplit('.', 1)
                    wiki = wiki[0]
                    self.wikis_time[wiki] = modify_time

    def mergerByYear(self):
        '''按年份来归并'''
        for i in self.wikis_time:
            year = str(self.wikis_time[i].tm_year)
            mergered_wikis_dic = self.mergered_all.get(year)
            if mergered_wikis_dic is None:
                dic = {i: self.wikis_time[i]}
                self.mergered_all[year] = dic
            else:
                mergered_wikis_dic[i] = self.wikis_time[i]

    def sortByTime(self):
        '''按时间排序'''
        for i in self.mergered_all:
            wikis_time = self.mergered_all[i]
            wikis_time_sorted = sorted(wikis_time.items(), key=lambda by: by[1], reverse=True)
            self.mergered_all[i] = wikis_time_sorted

    def sortByYear(self):
        self.mergered_all_sorted = sorted(self.mergered_all.items(), key=lambda by: by[0], reverse=True)

    def writeContent(self, f, year, wikis_time_sorted):
        if(len(wikis_time_sorted) > 0):
            print >>f, '%s' % year
        for wiki_info in wikis_time_sorted:
            splited_name = wiki_info[0].rsplit('.', 1)
            name = splited_name[0]
            if(name != WIKI_INDEX and name != 'search'):
                print >>f, '[[' + name + ']]'

    def writeContentIndex(self, f, wikis_info_sorted):
        for wiki_info in wikis_info_sorted:
            splited_name = wiki_info[0].rsplit('.', 1)
            name = splited_name[0]

            if(name != WIKI_INDEX and name != 'search' and name != 'todo-list' and (name[0] != 'p' and name[1] != '/')  # 以 p/ 打头的不能显示到 wiki_index
               and self.mergered_all.get(name) is None):
                print >>f, '| [[' + name + ']] |'

    def createWiki(self, year, wikis_times_sorted):
        wiki_name = year

        now_time = time.localtime()
        if(year == str(now_time.tm_year)):
            wiki_name = WIKI_INDEX
        f = open('%s.wiki' % wiki_name, 'w')
        #print >>f, '%nohtml'
        print >>f, "%title bigzhu's wiki"
        print >>f, ''
        print >>f, '''
        - 这是[[bigzhu]]%s年的wiki,[[vimwiki]]生成,是一些随手记下的零碎知识点,不适合浏览的.
        - 有条目没內容的(折騰的后果),给我[[mailto:vermiliondun@gmail.com|vermiliondun@gmail.com]]留言,我来生成html
        - 如果你是程序员,我在昆明且招人中......你懂的
        ''' % year

        if wiki_name != WIKI_INDEX:
            print >>f, '==[[%s|%s年的文章]]==' % (int(year) + 1, int(year) + 1)
            print >>f, ''
            self.writeContentIndex(f, wikis_times_sorted)
            print >>f, ''
            print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 1, int(year) - 1)
        else:
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year), int(year))
            self.writeContentIndex(f, wikis_times_sorted)
            print >>f, ''
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 1, int(year) - 1)
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 2, int(year) - 2)
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 3, int(year) - 3)
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 4, int(year) - 4)
            #print >>f, '==[[%s|%s年的文章]]==' % (int(year) - 5, int(year) - 5)
        f.close()

    def writeResult(self):
        if(self.wiki_name == '*'):
            for i in self.mergered_all:
                self.createWiki(i, self.mergered_all[i])
        f = open('search.wiki', 'w')
        print >>f, '%nohtml'
        for i in self.mergered_all_sorted:
            self.writeContent(f, i[0], i[1])
        print >>f, '[[%s]]' % self.wiki_name
        f.close()


def main():
    args = sys.argv
    if(len(args) == 1):
        print '请输入要查找的 wiki 关键字'
        exit()
    elif(len(args) == 2):
        name = args[1]
        seartch_wiki = SearchWiki(name)
        seartch_wiki.search()
        #seartch_wiki.search('p')
        seartch_wiki.mergerByYear()
        seartch_wiki.sortByTime()
        seartch_wiki.sortByYear()
        seartch_wiki.writeResult()

        #search_file = SearchFile(name)
        #if(search_file.pathExist()):
        #    search_file.search()
        #    search_file.sortByTime()
        #    search_file.writeResult()

if __name__ == '__main__':
    main()
    #import fnmatch
    #print fnmatch.fnmatchcase('我bigzhu.txt'.upper(), '*IGzhu.txt'.upper())
