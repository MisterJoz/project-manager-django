# Generated by Django 3.0.5 on 2020-05-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20200522_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='completion_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
