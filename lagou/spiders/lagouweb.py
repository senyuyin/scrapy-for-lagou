# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from urllib import parse
import json

from lagou import items


class LagouwebSpider(scrapy.Spider):

    name = 'lagouweb'

    url = 'https://www.lagou.com/jobs/positionAjax.json?'

    data = {
        'city':'上海',
        'needAddtionalResult':'false'
    }
    parseword = parse.urlencode(data)

    position_url = url + parseword

    cookies = {
    'cookies': ''
    }
    page = 1

    def start_requests(self):

        yield FormRequest(url=self.position_url, formdata={'first':'true', 'pn':str(self.page), 'kd':'python 爬虫'}, callback=self.job_parse, cookies=self.cookies)

    def job_parse(self, response):
        global page
        jdict = json.loads(response.text)
        print(jdict['success'])
        if jdict['success'] == False:
            yield FormRequest(url=self.position_url,formdata={'first': 'true', 'pn': str(self.page), 'kd': 'python 爬虫'}, callback=self.job_parse, cookies=self.cookies)

        try:
            position = jdict['content']['positionResult']['result']
        except KeyError:
            print('response failed')
            return None

        item = items.LagouItem()

        for n in range(0, len(position)):
            for field in item.fields:
                if field in position[n].keys():
                    item[field] = position[n].get(field)
            yield item

        if int(jdict['content']['pageNo']) != 0:
            print(int(jdict['content']['pageNo']))
            self.page = int(jdict['content']['pageNo'])
            yield FormRequest(url=self.position_url, formdata={'first':'false', 'pn':str(jdict['content']['pageNo']+1), 'kd':'python 爬虫'}, callback=self.job_parse, cookies=self.cookies)










