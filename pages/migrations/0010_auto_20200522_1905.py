# Generated by Django 3.0.5 on 2020-05-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20200522_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='final_total',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
