#!/usr/python/env
# -*- coding:utf-8 -*-
# Create by Feng.wei on 2016/10/20

from bs4 import BeautifulSoup as bs
import re
import trace

def readFile(path):
    f = open(path)
    page = f.read()
    f.close()
    return page

def parseHtml(path):
    soup = bs(readFile(path),'html.parser')
    tableList = soup.findAll('table')[2:]
    for table in tableList:
        print "==============="
        initRow = []
        tdCount = 0
        for tr in table.findAll('tr')[2:]:
            currRow = []
            for td in tr.findAll('td'):
                text = td.p.span.text.encode('utf-8')
                if tdCount == 0:
                    initRow.append(text)
                currRow.append(text)
            #print(splitCells(initRow, currRow))
            tdCount = tdCount + 1
            currRow = splitCells(initRow, currRow)
            for c in currRow:
                print(c + " "),
            print()
    print len(tableList)

def splitCells(initRow, currRow):
    i = len(initRow)
    c = len(currRow)
    for r in range(i - c):
       currRow.insert(r, initRow[r])
    print("======%d" %(len(currRow)))
    return currRow

if __name__ == '__main__':
    parseHtml('E:\personal\junligong\demo2.htm')
