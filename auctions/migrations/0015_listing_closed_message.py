# Generated by Django 3.0.8 on 2020-08-09 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200808_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed_message',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
