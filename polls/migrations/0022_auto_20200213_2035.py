# Generated by Django 2.2.6 on 2020-02-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_auto_20200104_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mapsurveyquestion',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='mapusersurvey',
            name='time_invited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
