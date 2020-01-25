from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
# Create your models here.


class dalabtest(models.Model):
    cdate = models.DateTimeField(null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    panel_purchase_amount_ave = models.FloatField(null=True)
    panel_purchase_amount_sum = models.FloatField(null=True)
    retail_price = models.FloatField(null=True)
    wholesale_price = models.FloatField(null=True)
    wholesale_amount_kg = models.CharField(max_length=100, null=True)
    output_kg_per_ha = models.CharField(max_length=100, null=True)
    area_ha = models.CharField(max_length=100, null=True)
    output_kg_year = models.CharField(max_length=100, null=True)
    output_kg_year_before = models.CharField(max_length=100, null=True)
    news_freq = models.CharField(max_length=100, null=True)
    Emotions_Number_Angries = models.CharField(max_length=100, null=True)
    Emotions_Number_likes = models.CharField(max_length=100, null=True)
    Emotions_Number_sads = models.CharField(max_length=100, null=True)
    Emotions_Number_wants = models.CharField(max_length=100, null=True)
    Emotions_Number_warms = models.CharField(max_length=100, null=True)
    news_comment_freq = models.CharField(max_length=100, null=True)
    news_positive_term_freq = models.CharField(max_length=100, null=True)
    news_negative_term_freq = models.CharField(max_length=100, null=True)
    video_freq = models.CharField(max_length=100, null=True)
    video_total_ranking_ave_p = models.CharField(max_length=100, null=True)
    video_freq_times_viewrate = models.CharField(max_length=100, null=True)
    video_positive_term_freq = models.CharField(max_length=100, null=True)
    blog_freq = models.CharField(max_length=100, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'new_collect'


class Feedback(models.Model):
    fullName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    feedback = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='new')
    adminComment = models.TextField(null=True)
    ipAddress = models.CharField(max_length=20)
    deviceInfo = models.CharField(max_length=200)
    objects = models.Manager()
