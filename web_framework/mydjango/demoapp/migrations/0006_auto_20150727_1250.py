# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0005_auto_20150727_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sort',
            field=models.SmallIntegerField(default=100, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f'),
        ),
    ]
