# Generated by Django 2.2 on 2019-04-17 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dalabtest',
            name='Emotions_Number_Angries',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='Emotions_Number_likes',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='Emotions_Number_sads',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='Emotions_Number_wants',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='Emotions_Number_warms',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='area_ha',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='month',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='news_comment_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='news_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='news_negative_term_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='news_positive_term_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='output_kg_per_ha',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='output_kg_year',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='output_kg_year_before',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='panel_purchase_amount',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='retail_price',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='video_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='video_freq_times_viewrate',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='video_positive_term_freq',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='video_total_ranking_ave_p',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='week',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='wholesale_amount_kg',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='wholesale_price',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dalabtest',
            name='year',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
