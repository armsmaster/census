# Generated by Django 2.2.6 on 2019-10-24 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20191021_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapusersurvey',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='polls.Survey'),
        ),
    ]
