# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0002_auto_20150727_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='date published',
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.CharField(default=b'', max_length=50, verbose_name='\u53d1\u5e03\u4eba'),
        ),
        migrations.AddField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 27, 12, 4, 28, 519109, tzinfo=utc), verbose_name='\u53d1\u5e03\u65e5\u671f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, verbose_name='\u95ee\u9898'),
        ),
    ]
