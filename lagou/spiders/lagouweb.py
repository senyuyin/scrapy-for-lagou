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

   # cookies = {
   #     'cookies':'user_trace_token=20170531130429-a02507f7-45be-11e7-953f-5254005c3644; LGUID=20170531130429-a0250d4b-45be-11e7-953f-5254005c3644; TG-TRACK-CODE=index_search; JSESSIONID=ABAAABAAAFCAAEG25EB2DFD44EEA5F13F5A64AC194BBAAC; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; _ga=GA1.2.61709395.1496207069; _gid=GA1.2.1471270549.1496555853; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1496135008,1496143729,1496393386,1496555853; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1496585909; LGSID=20170604221817-a797ba37-4930-11e7-9e39-525400f775ce; LGRID=20170604221829-ae683859-4930-11e7-9e39-525400f775ce; _putrc=E02723C0A1A4F26B; login=true; unick=%E5%BE%90%E7%AB%8B%E8%BE%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=2; SEARCH_ID=ffbaf1bb15cc4bafbe6a5f2d58dedc67; index_location_city=%E6%9D%AD%E5%B7%9E'
   #}

    page = 1

    def start_requests(self):

        yield FormRequest(url=self.position_url, formdata={'first':'true', 'pn':str(self.page), 'kd':'python 爬虫'}, callback=self.job_parse)

    def job_parse(self, response):
        global page
        jdict = json.loads(response.text)
        print(jdict['success'])

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
            yield FormRequest(url=self.position_url, formdata={'first':'false', 'pn':str(jdict['content']['pageNo']+1), 'kd':'python 爬虫'}, callback=self.job_parse)










