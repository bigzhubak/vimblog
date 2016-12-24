#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("./lib_p_bz")

import public_bz
import os
import fnmatch
import time
from public_bz import storage

import ConfigParser
config = ConfigParser.ConfigParser()
with open('conf.ini', 'r') as cfg_file:
    config.readfp(cfg_file)
    TITLE = config.get('data', 'title')
    HTML_PATH = config.get('data', 'html_path')


def getModifyTime(name):
    '''
    取文件的修改时间
    '''
    path_name = HTML_PATH + name + '.html'
    return time.localtime(os.path.getmtime(path_name))


def isNameLike(html_name, search_name):
    '''
    是否相似
    '''
    if search_name == '*':
        return True

    return fnmatch.fnmatchcase(html_name.upper(), ('*%s*' % search_name).upper())


def cutName(html):
    '''
    截取名字
    '''
    html_name = os.path.basename(html)
    html_name = html_name.rsplit('.', 1)
    html_name = html_name[0]
    return html_name


def getHtmlListByNameLike(search_name):
    '''
    根据名字查找对应html
    返回 list
    {name:'', time: ''}
    '''
    html_list = []
    for html in os.listdir(HTML_PATH):
        html_name = cutName(html)
        if html_name == '':
            continue
        if isNameLike(html_name, search_name):
            pass
        else:
            continue

        try:
            modify_time = getModifyTime(html_name)
        except OSError as e:  # 可能会有非html结尾的文件，忽略
            print e
            continue

        the_html = storage()
        the_html.name = html_name
        the_html.time = modify_time
        html_list.append(the_html)

    # 按时间排序
    html_list = sorted(html_list, key=lambda d: d.time, reverse=True)
    return html_list


def getHtmlContent(name):
    '''
    取得对应名字的 html 文件的内容
    '''
    try:
        name_file = open(HTML_PATH + name + '.html', 'r')
        content = name_file.read()
        name_file.close()
        return content
    except IOError:
        print public_bz.getExpInfoAll()
        return '0'


def getHtmlByName(name):
    the_html = storage()
    the_html.name = name
    the_html.time = getModifyTime(name)
    the_html.content = getHtmlContent(name)
    return the_html


def getMainList():
    '''
    取出前10个blog的内容
    '''
    html_list = getHtmlListByNameLike('*')
    html_list = html_list[:9]
    for html in html_list:
        html.content = getHtmlContent(html.name)
    return html_list


if __name__ == '__main__':
    for i in getMainList():
        print i
