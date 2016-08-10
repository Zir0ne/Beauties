#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 用于抓取知乎 """

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest


class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    urls = ['https://www.zhihu.com']
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'www.zhihu.com',
        'Origin': 'http://www.zhihu.com',
        'Referer': 'http://www.zhihu.com/',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def start_requests(self):
        return [Request('http://www.zhihu.com/login/phone_num', meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print('1: xsrf = ' + xsrf)
        self.headers['X-Xsrftoken'] = xsrf
        return [FormRequest.from_response(response,
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,
                                          formdata={'_xsrf': xsrf, 'phone_num': '18610722496', 'password': 'Marry@151001'},
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, response):
        for url in self.urls:
            print('2: after login: ' + url)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        print('3: print some pages')
        problem = Selector(response)
        print('3: url = ' + response.url)
        print('3: problem = ' + str(problem.xpath('//span[@class="name"]/text()').extract()))
        return
