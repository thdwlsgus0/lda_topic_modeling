# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from django.core.exceptions import ObjectDoesNotExist
from iCrawler.models import NaverBlog, DaumBlog, NaverNews, Twitter, MyCollection, MyCollectionDetail, MyCollectionStats
import json
import logging


class NaverBlogPipeline(object):

    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    def process_item(self, item, spider):

        try:
            collect = MyCollection.objects.get(unique_id=self.unique_id)
            if collect:
                blogUrl = item['url']
                addDetail = True

                try:
                    blog = Twitter.objects.get(url=blogUrl)
                except ObjectDoesNotExist:
                    blog = NaverBlog()
                    blog.search_keyword = item['searchKeyword']
                    blog.origin_keyword = item['originKeyword']
                    blog.item_type = item['itemType']
                    blog.category = item['category']
                    blog.sub_category = item['subCategory']
                    blog.url = item['url']
                    blog.title = item['title']
                    blog.date = item['date']
                    blog.content = item['content']
                    blog.no_likes = item['noLikes']
                    blog.no_images = item['noImages']
                    blog.no_comments = item['noComments']
                    blog.save()

                    detail = MyCollectionDetail()
                    detail.collection = collect
                    detail.naver_blog = blog
                    detail.save()
                except Exception as e:
                    addDetail = False
                    print('Naver Blog Pipline', str(e))

                if addDetail:
                    detail = MyCollectionDetail()
                    detail.collection = collect
                    detail.naver_blog = blog
                    detail.save()

        except Exception as e:
            print('Error Blog', str(e))

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            unique_id=crawler.settings.get('unique_id')
        )


class DaumBlogPipeline(object):

    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    def process_item(self, item, spider):
        try:
            collect = MyCollection.objects.get(unique_id=self.unique_id)
            if collect:
                blogUrl = item['url']
                addDetail = True

                try:
                    blog = DaumBlog.objects.get(url=blogUrl)
                except ObjectDoesNotExist:
                    blog = DaumBlog()
                    blog.search_keyword = item['searchKeyword']
                    blog.origin_keyword = item['originKeyword']
                    blog.item_type = item['itemType']
                    blog.category = item['category']
                    blog.sub_category = item['subCategory']
                    blog.url = item['url']
                    blog.title = item['title']
                    blog.date = item['date']
                    blog.content = item['content']
                    blog.no_likes = item['noLikes']
                    blog.no_images = item['noImages']
                    blog.no_comments = item['noComments']
                    blog.save()

                    detail = MyCollectionDetail()
                    detail.collection = collect
                    detail.daum_blog = blog
                    detail.save()
                except Exception as e:
                    addDetail = False
                    print('Naver Blog Pipline', str(e))

                if addDetail:
                    detail = MyCollectionDetail()
                    detail.collection = collect
                    detail.daum_blog = blog
                    detail.save()
        except Exception as e:
            print('Error Blog', str(e))

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            unique_id=crawler.settings.get('unique_id')
        )


class NaverNewsPipeline(object):

    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    def process_item(self, item, spider):

        try:
            collect = MyCollection.objects.get(unique_id=self.unique_id)
            if collect:
                blogUrl = item['url']
                addDetail = True

                try:
                    news = NaverNews.objects.get(url=blogUrl)
                except ObjectDoesNotExist:
                    news = NaverNews()
                    news.search_keyword = item['searchKeyword']
                    news.origin_keyword = item['originKeyword']
                    news.item_type = item['itemType']
                    news.category = item['category']
                    news.sub_category = item['subCategory']
                    news.url = item['url']
                    news.title = item['title']
                    news.publisher = item['publisher']
                    news.original_link = item['originalLink']
                    news.date = item['date']
                    news.content = item['content']

                    news.no_emotions = item['noEmotions']
                    news.no_e_likes = item['noELikes']
                    news.no_e_warms = item['noEWarms']
                    news.no_e_sads = item['noESads']
                    news.no_e_angries = item['noEAngries']
                    news.no_e_wants = item['noEWants']

                    news.no_images = item['noImages']
                    news.no_comments = item['noComments']
                    news.save()
                except Exception as e:
                    addDetail = False
                    print('Naver News Pipline', str(e))

                if addDetail:
                    detail = MyCollectionDetail()
                    detail.collection = collect
                    detail.naver_news = news
                    detail.save()

        except Exception as e:
            print('Error News', str(e))

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            unique_id=crawler.settings.get('unique_id')
        )


class TwitterPipeline(object):

    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    def process_item(self, item, spider):
        collect = MyCollection.objects.get(unique_id=self.unique_id)

        if collect:
            uname = item['username']
            tid = item['twitterId']
            addDetail = True

            try:
                tweet = Twitter.objects.get(
                    username=uname, twitter_id=tid)
            except ObjectDoesNotExist:
                tweet = Twitter()
                tweet.unique_id = item['jobId']
                tweet.search_keyword = item['searchKeyword']
                tweet.origin_keyword = item['originKeyword']
                tweet.item_type = item['itemType']
                tweet.category = item['category']
                tweet.sub_category = item['subCategory']
                tweet.url = item['url']
                tweet.username = item['username']
                tweet.twitter_id = item['twitterId']
                tweet.date = item['date']
                tweet.content = item['content']
                tweet.no_replies = item['noReplies']
                tweet.no_favorites = item['noFavorites']
                tweet.no_retweets = item['noRetweets']
                tweet.hash_tag = item['hashTag']
                tweet.mention = item['mention']
                tweet.geo_location = item['geoLocation']
                tweet.save()
            except Exception as e:
                addDetail = False
                print('Twitter Pipline', str(e))

            if addDetail:
                detail = MyCollectionDetail()
                detail.collection = collect
                detail.twitter = tweet
                detail.save()

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            unique_id=crawler.settings.get('unique_id')
        )
