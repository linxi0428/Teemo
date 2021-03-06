# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import requests
from lib import myparser
import time

class search_baidu:

    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name ="Baidu"
        self.word = word
        self.limit = int(limit)
        self.results = ""
        self.totalresults = ""
        self.proxies = proxy
        self.server = "www.baidu.com"
        self.headers = {'User-Agent': useragent}
        self.counter = 0 #

    def do_search(self):
        try:
            url = "http://{0}/s?wd={1}&pn={2}".format(self.server,self.word,self.counter)# 这里的pn参数是条目数
        except Exception, e:
            print e
        try:
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            self.results = r.content
            self.totalresults += self.results
        except Exception,e:
            print e

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            time.sleep(1)
            #print "\tSearching " + str(self.counter) + " results..."
            self.counter += 10

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        #print "%s email(s) found in Baidu" %len(rawres.emails())
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        #print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return rawres.hostnames()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        print "[-] {0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e))
        return self.d, self.e

def baidu(keyword, limit, useragent, proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_baidu(keyword, limit, useragent)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()

if __name__ == "__main__":
        useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        search = search_baidu("meizu.com", '100', useragent)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_hosts
        print all_emails#test successed
