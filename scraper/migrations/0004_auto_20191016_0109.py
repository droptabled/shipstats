# Generated by Django 2.2.6 on 2019-10-16 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_auto_20191015_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='wg_id',
            new_name='wg_user',
        ),
        migrations.RenameField(
            model_name='userstat',
            old_name='wg_id',
            new_name='wg_user',
        ),
    ]
