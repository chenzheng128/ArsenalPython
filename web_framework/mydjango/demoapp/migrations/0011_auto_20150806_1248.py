# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0010_auto_20150806_1245'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Article',
            new_name='D01Article',
        ),
        migrations.RenameModel(
            old_name='Reporter',
            new_name='D01Reporter',
        ),
    ]
