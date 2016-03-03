# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0011_auto_20150806_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='d02album',
            name='type',
            field=models.CharField(max_length=10, null=True, choices=[(b'CLA', b'\xe5\x8f\xa4\xe5\x85\xb8'), (b'POP', b'\xe7\x8e\xb0\xe4\xbb\xa3')]),
        ),
        migrations.AddField(
            model_name='d02album',
            name='type_int',
            field=models.IntegerField(null=True, choices=[(1, b'\xe6\x91\x87\xe6\xbb\x9a'), (2, b'\xe7\x88\xb5\xe5\xa3\xab')]),
        ),
    ]
