# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0009_question_checked'),
    ]

    operations = [
        migrations.CreateModel(
            name='D02Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('num_stars', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='D02Musician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('instrument', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='d02album',
            name='artist',
            field=models.ForeignKey(to='demoapp.D02Musician'),
        ),
    ]
