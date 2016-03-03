# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0008_auto_20150727_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='\u5ba1\u6838'),
        ),
    ]
