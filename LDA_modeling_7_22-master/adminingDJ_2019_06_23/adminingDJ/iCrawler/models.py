from django.db import models
from django.db.models import Aggregate, CharField
from django.utils import timezone

import json
# Create your models here.


class MyKeyword(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=100, null=True)
    main_category = models.CharField(max_length=100, null=True)
    middle_category = models.CharField(max_length=100, null=True)
    search_word = models.CharField(max_length=100, null=True)
    objects = models.Manager()


class MyCollection(models.Model):
    unique_id = models.CharField(max_length=200, null=True)
    jobids = models.CharField(max_length=250, null=True)
    search_keyword = models.CharField(max_length=250, null=True)

    channel_broadcast = models.CharField(max_length=250, null=True)
    channel_published = models.CharField(max_length=250, null=True)
    channel_blog = models.CharField(max_length=250, null=True)
    channel_sns = models.CharField(max_length=250, null=True)

    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    user_ip = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=100, null=True)

    status = models.CharField(default='pending', max_length=20)

    created_date = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    def addJobId(self, theId):
        ids = []
        try:
            ids = self.jobids.split(' ')
        except:
            ids = []
        ids.append(theId)
        self.jobids = ' '.join(ids)


class MyCollectionStats(models.Model):
    collection = models.ForeignKey(MyCollection, on_delete=models.CASCADE)
    search_keyword = models.CharField(max_length=250, null=True)
    channel = models.CharField(max_length=100, null=True)
    channel_sub = models.CharField(max_length=100, null=True)
    url = models.TextField(null=True)
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    content_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)

    num_comments = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_images = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_likes = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_replies = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_favorites = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_retweets = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_emotions = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_e_likes = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_e_warms = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_e_sads = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_e_angries = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    num_e_wants = models.PositiveIntegerField(
        default=None, null=True, blank=True)
    objects = models.Manager()


class NaverBlog(models.Model):

    unique_id = models.CharField(max_length=200, null=True)
    search_keyword = models.CharField(max_length=30, null=True)
    origin_keyword = models.CharField(max_length=30, null=True)
    item_type = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    sub_category = models.CharField(max_length=30, null=True)
    url = models.TextField(null=True)
    title = models.TextField(null=True)
    date = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    no_likes = models.IntegerField(null=True, default=0)
    no_images = models.IntegerField(null=True, default=0)
    no_comments = models.IntegerField(null=True, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    @property
    def to_dict(self):
        data = {
            "unique_id": json.loads(self.unique_id),
            "date": self.created_date
        }
        return data

    def __str__(self):
        return self.unique_id


class DaumBlog(models.Model):

    unique_id = models.CharField(max_length=200, null=True)
    search_keyword = models.CharField(max_length=30, null=True)
    origin_keyword = models.CharField(max_length=30, null=True)
    item_type = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    sub_category = models.CharField(max_length=30, null=True)
    url = models.TextField(null=True)
    title = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)
    content = models.TextField(null=True)
    no_likes = models.IntegerField(null=True, default=0)
    no_images = models.IntegerField(null=True, default=0)
    no_comments = models.IntegerField(null=True, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    @property
    def to_dict(self):
        data = {
            "unique_id": json.loads(self.unique_id),
            "date": self.created_date
        }
        return data

    def __str__(self):
        return self.unique_id


class Twitter(models.Model):
    unique_id = models.CharField(max_length=200, null=True)
    search_keyword = models.CharField(max_length=30,  null=True)
    origin_keyword = models.CharField(max_length=30,  null=True)
    item_type = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30,  null=True)
    sub_category = models.CharField(max_length=30,  null=True)
    url = models.TextField(null=True)
    username = models.CharField(max_length=100,  null=True)
    twitter_id = models.CharField(max_length=100,  null=True)
    date = models.DateTimeField(null=True)
    content = models.TextField(blank=True,  null=True)
    no_replies = models.IntegerField(blank=True,  null=True)
    no_favorites = models.IntegerField(blank=True,  null=True)
    no_retweets = models.IntegerField(blank=True,  null=True)
    hash_tag = models.TextField(null=True)
    mention = models.TextField(null=True)
    geo_location = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(default=timezone.now,  null=True)
    updated_date = models.DateTimeField(null=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.updated_date = timezone.now()
        super(Twitter, self).save(*args, **kwargs)

    @property
    def to_dict(self):
        data = {
            "unique_id": json.loads(self.unique_id),
            "date": self.created_date
        }
        return data

    def __str__(self):
        return self.unique_id


class NaverNews(models.Model):

    unique_id = models.CharField(max_length=200, null=True)
    search_keyword = models.CharField(max_length=30, null=True)
    origin_keyword = models.CharField(max_length=30, null=True)
    item_type = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    sub_category = models.CharField(max_length=30, null=True)
    url = models.TextField()
    title = models.TextField()
    publisher = models.CharField(max_length=100, null=True)
    original_link = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)
    content = models.TextField(null=True)
    no_emotions = models.IntegerField(null=True, default=0)
    no_e_likes = models.IntegerField(null=True, default=0)
    no_e_warms = models.IntegerField(null=True, default=0)
    no_e_sads = models.IntegerField(null=True, default=0)
    no_e_angries = models.IntegerField(null=True, default=0)
    no_e_wants = models.IntegerField(null=True, default=0)
    no_images = models.IntegerField(null=True, default=0)
    no_comments = models.IntegerField(null=True, default=0)

    created_date = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    @property
    def to_dict(self):
        data = {
            "unique_id": json.loads(self.unique_id),
            "date": self.created_date
        }
        return data

    def __str__(self):
        return self.unique_id


class MyCollectionDetail(models.Model):
    collection = models.ForeignKey(
        MyCollection, on_delete=models.SET_NULL, null=True)
    twitter = models.ForeignKey(Twitter, on_delete=models.SET_NULL, null=True)
    naver_news = models.ForeignKey(
        NaverNews, on_delete=models.SET_NULL, null=True)
    naver_blog = models.ForeignKey(
        NaverBlog, on_delete=models.SET_NULL, null=True)
    daum_blog = models.ForeignKey(
        DaumBlog, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
