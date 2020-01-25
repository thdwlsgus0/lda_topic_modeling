import scrapy
from scrappy_app.items import QuoteItem


class QuotesScraper(scrapy.Spider):
    name = "quotes"
    allowed_domain = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/js/'
    ]

    skipSelenium = False

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrappy_app.pipelines.QuotesPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrappy_app.middlewares.SeleniumMiddleware': 300
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        self.skipSelenium = not self.skipSelenium

        items = QuoteItem()

        all_div_quotes = response.css('div.quote')
        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tags = quote.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tags'] = tags
            items['url'] = response.url

            yield items

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
