import scrapy
import json
import re
import math
from scrapy.selector import Selector, HtmlXPathSelector
from urllib.parse import urlparse, urljoin, quote
from datetime import datetime
from scrappy_app.items import DaumBlogItem
from w3lib.html import remove_tags
from datetime import datetime
from iCrawler.models import MyCollection


class DaumBlogScraper(scrapy.Spider):
    name = "daum_blog"
    allowed_domain = ['blog.daum.net']

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrappy_app.pipelines.DaumBlogPipeline': 300
        }
    }

    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.get('keyword')
        self.termStart = kwargs.get('termStart')
        self.termEnd = kwargs.get('termEnd')

        self.jobId = kwargs.get('_job')
        uid = kwargs.get('uid')
        tweet = MyCollection.objects.get(unique_id=uid)
        if tweet:
            tweet.addJobId(self.jobId)
            tweet.save()
        super(DaumBlogScraper, self).__init__(*args, **kwargs)

    def start_requests(self):
        keywords = self.keyword.split(",")
        termStart = self.termStart.replace('-', '')
        termEnd = self.termEnd.replace('-', '')
        start = 1
        for kw in keywords:
            url = 'http://search.daum.net/search?q={}&w=blog&f=section&SA=daumsec&DA=PGD&lpp=10&nil_search=btn&sd={}000000&ed={}235959&period=u&enc=utf8&page={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start
            )
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

        # for aUrl in self.start_urls:

    def parse_search(self, response):
        kw = response.meta.get('keyword')
        termStart = response.meta.get('termStart')
        termEnd = response.meta.get('termEnd')
        start = int(response.meta.get('start')) + 1

        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="f_link_b"]//@href').extract()
        for url in urls:
            if url is not None:
                url = response.urljoin(url)
                parsed = urlparse(url)
                replaced = parsed._replace(netloc="m.blog.daum.net")
                url = replaced.geturl()
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw})

        allRows = hxs.xpath(
            '//div[@class="sub_expander"]/span[@class="txt_info"]/text()').extract_first()
        numDocs = self.countPages(allRows)
        print(start, numDocs)
        if start <= numDocs:
            url = 'http://search.daum.net/search?q={}&w=blog&f=section&SA=daumsec&DA=PGD&lpp=10&nil_search=btn&sd={}000000&ed={}235959&period=u&enc=utf8&page={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start
            )
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

    def parse_blog(self, response):
        kw = response.meta.get('keyword')
        hxs = Selector(response)

        url = hxs.xpath('//frame/@src').extract_first()

        if url is not None:
            url = urljoin('http://blog.daum.net', url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw})

    def parse(self, response):
        kw = response.meta.get('keyword')
        hxs = Selector(response)

        items = DaumBlogItem()

        title = hxs.xpath('//h3[@class="tit_view"]/text()').extract_first()
        if title is None:
            title = ""
        else:
            title = title.strip()

        date = hxs.xpath(
            '//time[@class="txt_time"]/text()').extract_first()
        if date is None:
            date = ""

        content = hxs.css(
            'div#article ::text').extract()
        if content is None:
            content = ""
        else:
            content = ' '.join(content)
            content = content.strip()

        noImages = hxs.xpath(
            '//div[@id="article"]//img').extract()
        if noImages is None:
            noImages = 0
        else:
            noImages = len(noImages)

        noComments = hxs.css(
            'div.use_btns span.txt_num::text').extract_first()
        if noComments is not None:
            noComments = int(noComments.strip())
        else:
            noComments = 0

        noLikes = hxs.xpath(
            '//a[@class="thisPostToDo"]/following-sibling::a/text()').extract_first()
        if noLikes is not None:
            noLikes = int(noLikes.replace('(', '').replace(')', '').strip())
        else:
            noLikes = 0

        items['searchKeyword'] = kw
        items['originKeyword'] = kw
        items['channel'] = 'blogs'
        items['channel_sub'] = 'daum'
        items['url'] = response.url
        items['date'] = date
        items['content'] = content
        items['title'] = title
        items['date'] = self.toDateTime(date)
        items['content'] = content
        items['noLikes'] = noLikes
        items['noImages'] = noImages
        items['noComments'] = noComments
        items['itemType'] = 'blog'
        items['category'] = 'blog'
        items['subCategory'] = 'daum'

        return items

    def toDateTime(self, strDateTime):
        try:
            return datetime.strptime(strDateTime, '%Y.%m.%d %H:%M')
        except Exception:
            return None

    def countPages(self, numOfDoc):
        cn = 1
        try:
            nums = numOfDoc.split(' / ')
            docs = int(nums[1].replace('건', ''))
            cn = math.ceil(docs/10)
        except Exception as e:
            print('Daum Blog Count Docs', str(e))

        if cn > 100:
            cn = 100
        return cn
