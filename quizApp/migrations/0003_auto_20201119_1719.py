# Generated by Django 3.1.3 on 2020-11-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0002_auto_20201119_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='date_finished',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
