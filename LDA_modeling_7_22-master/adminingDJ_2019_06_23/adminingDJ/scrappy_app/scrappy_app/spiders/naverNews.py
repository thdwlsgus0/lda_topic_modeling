import scrapy
import json
import re
from scrapy.selector import Selector, HtmlXPathSelector
from urllib.parse import urlparse, urljoin, quote
from datetime import datetime
from scrappy_app.items import NaverNewsItem
from iCrawler.models import MyCollection


class NaverNewsScraper(scrapy.Spider):
    name = "naver_news"
    allowed_domain = ['news.naver.com', 'search.naver.com']

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrappy_app.pipelines.NaverNewsPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrappy_app.middlewares.SeleniumMiddleware': 300
        }
    }

    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.get('keyword')
        self.termStart = kwargs.get('termStart')
        self.termEnd = kwargs.get('termEnd')
        self.mediaName_bc = kwargs.get('mediaName_bc')
        self.mediaName_pn = kwargs.get('mediaName_pn')
        self.jobId = kwargs.get('_job')
        uid = kwargs.get('uid')
        tweet = MyCollection.objects.get(unique_id=uid)
        if tweet:
            tweet.addJobId(self.jobId)
            tweet.save()
        super(NaverNewsScraper, self).__init__(*args, **kwargs)

    def start_requests(self):
        keywords = self.keyword.split(",")
        termStart = self.termStart.replace('-', '.')
        termEnd = self.termEnd.replace('-', '.')
        start = 1

        for kw in keywords:
            url = 'https://search.naver.com/search.naver?ie=utf8&where=news&query={}&sm=tab_pge&sort=1&photo=0&field=0&pd=3&ds={}&de={}&qvt=0&start={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start)
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

    def parse_search(self, response):
        kw = response.meta.get('keyword')
        termStart = response.meta.get('termStart')
        termEnd = response.meta.get('termEnd')
        start = int(response.meta.get('start')) + 10

        hxs = Selector(response)
        urls = hxs.xpath(
            '//a[@class="_sp_each_url"]/@href').extract()
        for url in urls:
            if url is not None:
                url = response.urljoin(url)
                self.logger.warning(url)
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw})

        allRows = hxs.xpath(
            '//div[@class="title_desc all_my"]/span/text()').extract_first()
        numDocs = self.countDocs(allRows)
        if start < numDocs:
            url = 'https://search.naver.com/search.naver?ie=utf8&where=news&query={}&sm=tab_pge&sort=1&photo=0&field=0&pd=3&ds={}&de={}&qvt=0&start={}'.format(
                quote(kw), quote(termStart), quote(termEnd), start)
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'keyword': kw, 'termStart': termStart, 'termEnd': termEnd, 'start': start})

    def parse(self, response):
        kw = response.meta.get('keyword')
        hxs = Selector(response)

        items = NaverNewsItem()

        title = hxs.xpath(
            '//h3[@id="articleTitle"]/text()').extract_first()

        if title is None:
            title = hxs.xpath(
                '//span[@class="head_tit"]/text()').extract_first()
        if title is None:
            title = ""

        publisher = hxs.xpath(
            '//div[@class="press_logo"]/a/img/@alt').extract_first()
        if publisher is None:
            publisher = ""

        originalLink = hxs.xpath(
            '//div[@class="sponsor"]/a[@class="btn_artialoriginal"]/@href').extract_first()
        if originalLink is None:
            originalLink = ""

        date = hxs.xpath(
            '//span[@class="t11"]/text()').extract_first()
        if date is None:
            date = ""

        content = hxs.css(
            'div#articleBodyContents ::text').extract()
        if content is None:
            content = ""
        else:
            content = ''.join(content)
            content = ' '.join(content.split())

        noImages = hxs.xpath(
            '//div[@id="articleBody"]//img').extract()

        if noImages is None:
            noImages = 0
        else:
            noImages = len(noImages)

        noComments = hxs.xpath(
            '//span[@class="u_cbox_info_txt"]/text()').extract_first()
        if noComments is None:
            noComments = hxs.xpath(
                '//em[@class="simplecmt_num"]/text()').extract_first()

        if noComments is not None:
            noComments = int(noComments.strip())
        else:
            noComments = 0

        noEmotions = hxs.css(
            'span.u_likeit_text._count.num::text').extract_first()
        if noEmotions is None:
            noEmotions = 0
        else:
            noEmotions = int(noEmotions.sprit())

        noELikes = hxs.xpath(
            '//li[@class="u_likeit_list good"]//span[@class="u_likeit_text _count num"]/text()').extract_first()
        if noELikes is None:
            noELikes = 0

        noEWarms = hxs.xpath(
            '//li[@class="u_likeit_list warm"]/span[@class="u_likeit_list_count _count"]/text()').extract_first()
        if noEWarms is None:
            noEWarms = 0

        noESads = hxs.xpath(
            '//li[@class="u_likeit_list sad"]/span[@class="u_likeit_list_count _count"]/text()').extract_first()
        if noESads is None:
            noESads = 0

        noEAngries = hxs.xpath(
            '//li[@class="u_likeit_list angry"]/span[@class="u_likeit_list_count _count"]/text()').extract_first()
        if noEAngries is None:
            noEAngries = 0

        noEWants = hxs.xpath(
            '//li[@class="u_likeit_list want"]/span[@class="u_likeit_list_count _count"]/text()').extract_first()
        if noEWants is None:
            noEWants = 0

        items['searchKeyword'] = kw
        items['originKeyword'] = kw

        items['channel'] = 'news'
        items['channel_sub'] = publisher

        items['itemType'] = 'news'
        items['category'] = 'news'
        items['subCategory'] = 'news'
        items['publisher'] = publisher
        items['originalLink'] = originalLink

        items['url'] = response.url
        items['title'] = title
        items['date'] = self.toDateTime(date)
        items['content'] = content

        items['noImages'] = noImages
        items['noComments'] = noComments
        items['noEmotions'] = noEmotions
        items['noELikes'] = noELikes
        items['noEWarms'] = noEWarms
        items['noESads'] = noESads
        items['noEAngries'] = noEAngries
        items['noEWants'] = noEWants

        return items

    def toDateTime(self, strDateTime):
        try:
            strDateTime = strDateTime.replace('오후', 'PM')
            strDateTime = strDateTime.replace('오전', 'AM')

            print(strDateTime)
            return datetime.strptime(strDateTime, '%Y.%m.%d. %p %H:%M')
        except Exception:
            return None

    # def mediaList(self, channelName) {
    #     broadcastList = ["뉴시스", "SBS 뉴스", "MBC 뉴스", "YTN", "MBN", "한국경제TV", "SBS CNBC","뉴스1","채널A","enews24","KBS 연예","JTBC","KBS 뉴스","SBS funE","연합뉴스TV","TV조선","채널A"]

    # }
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
