
from djongo import models
from django import forms
from jsonfield import JSONField
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Twitter2010(models.Model):
    pass


class TrendWithSales(models.Model):
    cdate = models.DateTimeField(null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)

    panel_purchase_amount_ave = models.FloatField(null=True)
    panel_purchase_amount_sum = models.FloatField(null=True)
    retail_price = models.FloatField(null=True)
    wholesale_price = models.FloatField(null=True)

    news_freq = models.IntegerField(null=True)
    video_freq = models.IntegerField(null=True)
    blog_freq = models.IntegerField(null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'new_collection2'
class publish_onion(models.Model):
    Search_keyword = models.CharField(max_length=100, null=True)
    Date = models.DateTimeField(null=True)
    Content = models.CharField(max_length=10000, null=True)
    Title = models.CharField(max_length=100, null=True)
    cdate = models.DateTimeField(null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'published_onion'     

class TrendWithItemFreq(models.Model):
    cdate = models.DateTimeField(null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)

    channel = models.CharField(max_length=100, null=True)
    sub_channel = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    sub_category = models.CharField(max_length=100, null=True)
    tags = models.CharField(max_length=200, null=True)

    item_freq = models.IntegerField(null=True, default=0)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'mediaItemFrequency'
class keyword_insert(models.Model):
    Search_keyword = models.CharField(max_length=100, null=True)
    Date = models.DateTimeField(null=True)
    Content = models.CharField(max_length=10000, null=True)
    Title = models.CharField(max_length=100, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'onion2'
class word_count(models.Model):
    keyword = models.CharField(max_length=100, null=True)
    count = models.IntegerField(null=True)
    class Meta:
        abstract = True
        
class topic_class(models.Model):
    Search_keyword = models.CharField(max_length=100, null=True)
    Title = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    cdate = models.DateTimeField(null=True)
    total_date = models.CharField(max_length=100, null=True)
    keyword_list = models.CharField(max_length=200, null=True)
    count_list = models.CharField(max_length=200, null=True)
    #keyword_list = ArrayField(models.CharField(max_length=200), size=3)
    #count_list = ArrayField(models.IntegerField(), size=3)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'topic_result'
class practice(models.Model):
    Search_keyword = models.CharField(max_length=100, null=True)
    Title = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    cdate = models.DateTimeField(null=True)
    total_date = models.CharField(max_length=100, null=True)
    the_json = ArrayField(JSONField(default=dict))
    #keyword_list = ArrayField(models.CharField(max_length=200), size=3)
    #count_list = ArrayField(models.IntegerField(), size=3)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'practice'