# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0006_auto_20150727_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe', to='demoapp.Tag', blank=True),
        ),
    ]
