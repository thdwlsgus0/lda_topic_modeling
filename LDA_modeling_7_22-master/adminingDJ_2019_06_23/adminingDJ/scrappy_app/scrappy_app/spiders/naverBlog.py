import scrapy
import json
import re
from scrapy.selector import Selector, HtmlXPathSelector
from urllib.parse import urlparse, urljoin, quote, parse_qs
from datetime import datetime
from scrappy_app.items import NaverBlogItem
from datetime import datetime, timedelta
from iCrawler.models import MyCollection


class NaverBlogScraper(scrapy.Spider):
    name = "naver_blog"
    allowed_domain = ['blog.naver.com']

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrappy_app.pipelines.NaverBlogPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrappy_app.middlewares.SeleniumMiddleware': 300
        }
    }

    skipSelenium = True

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
        super(NaverBlogScraper, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.skipSelenium = True
        keywords = self.keyword.split(",")
        termStart = self.termStart.replace('-', '')
        termEnd = self.termEnd.replace('-', '')
        start = 1

        for kw in keywords:
            url = 'https://search.naver.com/search.naver?where=post&query={}&st=date&sm=tab_opt&date_from={}&date_to={}&date_option=8&srchby=all&dup_remove=1&qvt=0&start={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start)
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

        # for aUrl in self.start_urls:

    def parse_search(self, response):
        kw = response.meta.get('keyword')
        termStart = response.meta.get('termStart')
        termEnd = response.meta.get('termEnd')
        start = int(response.meta.get('start')) + 10

        hxs = Selector(response)
        urls = hxs.xpath(
            '//a[@class="sh_blog_title _sp_each_url _sp_each_title"]/@href').extract()

        for url in urls:
            if url is not None:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_blog, meta={'keyword': kw})

        allRows = hxs.xpath(
            '//span[@class="title_num"]/text()').extract_first()

        numDocs = self.countDocs(allRows)

        if start < numDocs:
            url = 'https://search.naver.com/search.naver?where=post&query={}&st=date&sm=tab_opt&date_from={}&date_to={}&date_option=8&srchby=all&dup_remove=1&qvt=0&start={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start)
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

    def parse_blog(self, response):
        kw = response.meta.get('keyword')
        hxs = Selector(response)

        url = hxs.xpath('//iframe[@id="mainFrame"]/@src').extract_first()
        self.skipSelenium = False
        if url is not None:
            url = urljoin('https://blog.naver.com', url)
            url = self.replaceUrl(url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw})

    def parse(self, response):
        kw = response.meta.get('keyword')
        hxs = Selector(response)

        items = NaverBlogItem()

        title = hxs.xpath(
            '//div[@class="se-module se-module-text se-title-text"]/p/span/text()').extract_first()
        if title is None:
            title = hxs.xpath(
                '//h3[@class="se_textarea"]/text()').extract_first()
            if title is None:
                title = ""

        date = hxs.xpath(
            '//span[@class="se_publishDate pcol2"]/text()').extract_first()
        if date is None:
            date = ""

        content = hxs.css(
            'div.se-main-container ::text').extract()

        if content is None:
            content = ""
        else:
            content = ''.join(content)
            content = ' '.join(content.split())

        noImages = hxs.xpath(
            '//div[@class="se-main-container"]//img').extract()

        if noImages is None:
            noImages = 0
        else:
            noImages = len(noImages)

        noComments = hxs.xpath(
            '//div[@class="area_comment pcol2"]/a/em/text()').extract_first()
        if noComments:
            noComments = int(noComments.strip())
        else:
            noComments = 0

        noLikes = hxs.xpath(
            '//em[@class="u_cnt _count"]/text()').extract_first()
        if noLikes:
            noLikes = int(noLikes.strip())
        else:
            noLikes = 0

        items['searchKeyword'] = kw
        items['originKeyword'] = kw
        items['channel'] = 'blogs'
        items['channel_sub'] = 'naver'
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
        items['subCategory'] = 'naver'

        yield items

    def replaceUrl(self, url):
        try:
            parsed = urlparse(url)
            blogId = parse_qs(parsed.query)['blogId'][0]
            logNo = parse_qs(parsed.query)['logNo'][0]

            res = 'http://blog.naver.com/PostView.nhn?blogId={0}&logNo={1}&redirect=Log&widgetTypeCall=false&directAccess=true'.format(
                blogId, logNo)
            return res
        except Exception:
            return url

    def toDateTime(self, strDateTime):
        try:
            return datetime.strptime(strDateTime, '%Y. %m. %d. %H:%M')
        except Exception:
            try:
                strDateTime = int(strDateTime.replace('시간 전', ''))
                return datetime.now() + timedelta(hours=-strDateTime)
            except:
                return None

    def countDocs(self, numOfDoc):
        cn = 0
        try:
            nums = numOfDoc.split(' / ')
            cn = int(nums[1].replace('건', ''))
        except Exception as e:
            print('Naver Blog Count Docs', str(e))

        if cn > 1000:
            cn = 1000
        return cn
