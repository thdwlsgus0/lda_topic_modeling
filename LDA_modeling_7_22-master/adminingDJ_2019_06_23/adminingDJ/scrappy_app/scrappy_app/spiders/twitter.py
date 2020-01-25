import scrapy
import json
import re
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import HtmlResponse
from urllib.parse import urlparse, urljoin, quote
from datetime import datetime
from scrappy_app.items import TwitterItem
from w3lib.html import remove_tags
from iCrawler.models import MyCollection


class TwitterScraper(scrapy.Spider):
    name = "twitter"
    allowed_domain = ['twitter.com']

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrappy_app.pipelines.TwitterPipeline': 300
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
        super(TwitterScraper, self).__init__(*args, **kwargs)

    def start_requests(self):
        keywords = self.keyword.split(",")
        for kw in keywords:
            kwFull = kw + ' since:' + self.termStart + ' until:' + self.termEnd
            url = 'https://twitter.com/i/search/timeline?&q={}&src=typd&max_position={}'.format(
                quote(kwFull), quote(''))
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw, 'keyword_full': kwFull})

        # for aUrl in self.start_urls:

    def parse(self, response):
        kw = response.meta.get('keyword')
        kwFull = response.meta.get('keyword_full')

        load_json = json.loads(response.text)
        items_html = load_json.get('items_html')
        html_response = HtmlResponse(
            url="HTML", body=items_html, encoding='utf-8')

        hxs = Selector(html_response)

        tweets = hxs.css('div.js-stream-tweet').extract()

        for tweet in tweets:
            html_response = HtmlResponse(
                url="HTML", body=tweet, encoding='utf-8')
            hxs = Selector(html_response)

            tweetId = hxs.xpath(
                "//div/@data-tweet-id").extract_first(default='')

            permalink = hxs.xpath(
                "//div/@data-permalink-path").extract_first(default='')

            username = hxs.css(
                'span.username.u-dir.u-textTruncate b::text').extract_first(default='')

            replies = int(hxs.css(
                'span.ProfileTweet-action--reply span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract_first(default=0))

            retweets = int(hxs.css(
                'span.ProfileTweet-action--retweet span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract_first(default=0))

            favorites = int(hxs.css(
                'span.ProfileTweet-action--favorite span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract_first(default=0))

            content = hxs.css(
                'p.js-tweet-text ::text').extract()
            if content is None:
                content = ""
            else:
                content = ''.join(content)

            date = hxs.css(
                'span.js-short-timestamp').xpath('@data-time').extract_first()
            if date is not None:
                date = datetime.fromtimestamp(int(date))

            geo = hxs.xpath(
                '//span[@class="Tweet-geo"]/@title').extract_first()
            if geo is None:
                geo = ""

            mention = self.lookupPatterns('@', content)
            hashtags = self.lookupPatterns('#', content)

            items = TwitterItem()

            items['jobId'] = self.jobId

            items['searchKeyword'] = kw
            items['originKeyword'] = kw
            items['itemType'] = 'twitter'
            items['category'] = 'twitter'
            items['subCategory'] = 'twitter'
            items['url'] = urljoin('https://twitter.com', permalink)
            items['username'] = username
            items['twitterId'] = tweetId
            items['date'] = date
            items['content'] = content
            items['noReplies'] = replies
            items['noFavorites'] = favorites
            items['noRetweets'] = retweets
            items['hashTag'] = hashtags
            items['mention'] = mention
            items['geoLocation'] = geo

            yield items

        has_more_items = load_json.get('has_more_items')
        print('has_more_items', has_more_items)
        if has_more_items:
            min_position = load_json.get('min_position')
            url = 'https://twitter.com/i/search/timeline?&q={}&src=typd&max_position={}'.format(
                quote(kwFull), min_position)
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': kw, 'keyword_full': kwFull})

    def lookupPatterns(self, patternS, baseText):
        words = [tag for tag in baseText.split() if tag.startswith(patternS)]
        return ' '.join(words)
