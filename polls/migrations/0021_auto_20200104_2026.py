# Generated by Django 2.2.6 on 2020-01-04 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20200104_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiongroup',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='polls.QuestionGroup'),
        ),
    ]
