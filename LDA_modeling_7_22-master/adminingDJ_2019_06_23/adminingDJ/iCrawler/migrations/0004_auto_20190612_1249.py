# Generated by Django 2.2 on 2019-06-12 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iCrawler', '0003_auto_20190612_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycollection',
            name='user_agent',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mycollection',
            name='user_ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]