# Generated by Django 2.2.6 on 2019-11-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20191112_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='data_num',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
