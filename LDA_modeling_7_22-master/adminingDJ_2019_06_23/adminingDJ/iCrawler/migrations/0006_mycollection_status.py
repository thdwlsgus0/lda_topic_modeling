# Generated by Django 2.2 on 2019-06-13 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iCrawler', '0005_auto_20190612_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycollection',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
