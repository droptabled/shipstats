# Generated by Django 3.0.4 on 2020-04-18 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popularity', '0002_auto_20200416_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shiprelation',
            old_name='count',
            new_name='playercount',
        ),
    ]