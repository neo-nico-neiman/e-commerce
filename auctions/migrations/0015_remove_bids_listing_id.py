# Generated by Django 3.1 on 2020-08-30 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200830_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='listing_id',
        ),
    ]