# Generated by Django 3.0.6 on 2020-08-22 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=1),
        ),
    ]
