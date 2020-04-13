# Generated by Django 3.0.4 on 2020-04-04 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_auto_20200331_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_primary_5th',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_primary_95th',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_primary_median',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_primary_q1',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_primary_q3',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_secondary_5th',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_secondary_95th',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_secondary_median',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_secondary_q1',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_secondary_q3',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='boxplotstat',
            name='ship_top_range',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_type',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Box'), (2, 'Scatter')]),
        ),
    ]
