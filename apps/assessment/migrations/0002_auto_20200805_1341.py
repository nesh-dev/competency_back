# Generated by Django 3.0.9 on 2020-08-05 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfassessmentaverage',
            name='assessee',
        ),
        migrations.RemoveField(
            model_name='selfassessmentaverage',
            name='competency',
        ),
        migrations.DeleteModel(
            name='PersonAssessingAverage',
        ),
        migrations.DeleteModel(
            name='SelfAssessmentAverage',
        ),
    ]
