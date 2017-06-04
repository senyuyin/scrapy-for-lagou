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
        'Cookie':'JSESSIONID=ABAAABAACBHABBI77FD495800B0E05F6D33D965B5A17EF8; user_trace_token=20170531130429-a02507f7-45be-11e7-953f-5254005c3644; LGUID=20170531130429-a0250d4b-45be-11e7-953f-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; _gat=1; _ga=GA1.2.61709395.1496207069; _gid=GA1.2.2057646644.1496208160; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1495975969,1496135008,1496143729; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1496217115; LGSID=20170531143955-f5741226-45cb-11e7-9542-5254005c3644; LGRID=20170531155155-046f5de1-45d6-11e7-8266-525400f775ce; SEARCH_ID=2f1b98280a2e4f5eb13e32a450fb21b1'
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










