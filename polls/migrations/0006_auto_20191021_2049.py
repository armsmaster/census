# Generated by Django 2.2.6 on 2019-10-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_mapusersurvey_random_letters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapusersurvey',
            name='random_letters',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
