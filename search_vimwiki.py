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

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_INDEX = 'wiki_index'


class SearchWiki:
    def __init__(self, wiki_name):
        self.wiki_name = wiki_name
        self.mergered_all = {}
        self.mergered_all_sorted = []
        self.wikis_time = {}

    def getHtmlNameList(self):
        html_list = []
        for html in os.listdir(HTML_PATH):
            html = os.path.basename(html)
            html = html.rsplit('.', 1)
            html = html[0]
            html_list.append(html)
        return html_list


    def search(self, path='.'):
        '''找到wiki文件名,并加上时间'''
        #wiki_names = glob.glob('*%s*.wiki' % self.wiki_name)
        html_list = self.getHtmlNameList()
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
                    if wiki in html_list:
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

if __name__ == '__main__':
    pass
    #import fnmatch
    #print fnmatch.fnmatchcase('我bigzhu.txt'.upper(), '*IGzhu.txt'.upper())
