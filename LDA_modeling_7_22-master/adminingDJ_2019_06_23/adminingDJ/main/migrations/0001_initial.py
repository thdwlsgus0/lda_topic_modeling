# Generated by Django 2.2 on 2019-04-17 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dalabtest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=100)),
                ('month', models.CharField(max_length=100)),
                ('week', models.CharField(max_length=100)),
                ('panel_purchase_amount', models.CharField(max_length=100)),
                ('retail_price', models.CharField(max_length=100)),
                ('wholesale_price', models.CharField(max_length=100)),
                ('wholesale_amount_kg', models.CharField(max_length=100)),
                ('output_kg_per_ha', models.CharField(max_length=100)),
                ('area_ha', models.CharField(max_length=100)),
                ('output_kg_year', models.CharField(max_length=100)),
                ('output_kg_year_before', models.CharField(max_length=100)),
                ('news_freq', models.CharField(max_length=100)),
                ('Emotions_Number_Angries', models.CharField(max_length=100)),
                ('Emotions_Number_likes', models.CharField(max_length=100)),
                ('Emotions_Number_sads', models.CharField(max_length=100)),
                ('Emotions_Number_wants', models.CharField(max_length=100)),
                ('Emotions_Number_warms', models.CharField(max_length=100)),
                ('news_comment_freq', models.CharField(max_length=100)),
                ('news_positive_term_freq', models.CharField(max_length=100)),
                ('news_negative_term_freq', models.CharField(max_length=100)),
                ('video_freq', models.CharField(max_length=100)),
                ('video_total_ranking_ave_p', models.CharField(max_length=100)),
                ('video_freq_times_viewrate', models.CharField(max_length=100)),
                ('video_positive_term_freq', models.CharField(max_length=100)),
            ],
        ),
    ]
