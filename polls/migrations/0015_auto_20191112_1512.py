# Generated by Django 2.2.6 on 2019-11-12 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_answer_data_num'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mapsurveyquestion',
            unique_together={('survey', 'question')},
        ),
    ]
