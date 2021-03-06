# Generated by Django 2.2 on 2019-06-12 03:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iCrawler', '0002_mycollection_mycollectionstats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycollection',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='mycollection',
            name='channel_sub',
        ),
        migrations.RemoveField(
            model_name='mycollection',
            name='content',
        ),
        migrations.RemoveField(
            model_name='mycollection',
            name='content_date',
        ),
        migrations.RemoveField(
            model_name='mycollection',
            name='title',
        ),
        migrations.RemoveField(
            model_name='mycollection',
            name='url',
        ),
        migrations.AddField(
            model_name='mycollection',
            name='channel_blog',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='channel_broadcast',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='channel_published',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='channel_sns',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='mycollectionstats',
            name='channel_sub',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mycollectionstats',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mycollectionstats',
            name='content_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='mycollectionstats',
            name='title',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mycollectionstats',
            name='url',
            field=models.TextField(null=True),
        ),
    ]
