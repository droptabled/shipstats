# Generated by Django 2.2.6 on 2019-10-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20191015_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstat',
            name='ship_id',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
