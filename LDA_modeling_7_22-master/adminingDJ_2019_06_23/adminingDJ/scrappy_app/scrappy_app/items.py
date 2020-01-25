# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from django.utils import timezone


class TwitterItem(scrapy.Item):
    jobId = scrapy.Field()
    searchKeyword = scrapy.Field()
    channel = scrapy.Field()
    channel_sub = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    noReplies = scrapy.Field()
    noFavorites = scrapy.Field()
    noRetweets = scrapy.Field()
    hashTag = scrapy.Field()
    mention = scrapy.Field()
    geoLocation = scrapy.Field()
    originKeyword = scrapy.Field()
    category = scrapy.Field()
    subCategory = scrapy.Field()
    itemType = scrapy.Field()
    username = scrapy.Field()
    twitterId = scrapy.Field()


class NaverBlogItem(scrapy.Item):
    searchKeyword = scrapy.Field()
    channel = scrapy.Field()
    channel_sub = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    noLikes = scrapy.Field()
    noImages = scrapy.Field()
    noComments = scrapy.Field()

    originKeyword = scrapy.Field()
    itemType = scrapy.Field()
    category = scrapy.Field()
    subCategory = scrapy.Field()


class DaumBlogItem(scrapy.Item):
    searchKeyword = scrapy.Field()
    channel = scrapy.Field()
    channel_sub = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    noLikes = scrapy.Field()
    noImages = scrapy.Field()
    noComments = scrapy.Field()
    originKeyword = scrapy.Field()
    itemType = scrapy.Field()
    category = scrapy.Field()
    subCategory = scrapy.Field()


class NaverNewsItem(scrapy.Item):
    searchKeyword = scrapy.Field()
    channel = scrapy.Field()
    channel_sub = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    noEmotions = scrapy.Field()
    noELikes = scrapy.Field()
    noEWarms = scrapy.Field()
    noESads = scrapy.Field()
    noEAngries = scrapy.Field()
    noEWants = scrapy.Field()
    noImages = scrapy.Field()
    noComments = scrapy.Field()

    originKeyword = scrapy.Field()
    itemType = scrapy.Field()
    category = scrapy.Field()
    subCategory = scrapy.Field()
    publisher = scrapy.Field()
    originalLink = scrapy.Field()


class QuoteItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    created_date = scrapy.Field()
