# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0003_auto_20150727_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['sort'], 'verbose_name': '\u9009\u9879', 'verbose_name_plural': '\u9009\u9879\u7ba1\u7406'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u6295\u7968\u95ee\u9898', 'verbose_name_plural': '\u6295\u7968\u95ee\u9898\u7ba1\u7406'},
        ),
        migrations.AddField(
            model_name='choice',
            name='sort',
            field=models.SmallIntegerField(default=100, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200, verbose_name='\u9009\u9879'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='\u6295\u7968\u6570'),
        ),
    ]
