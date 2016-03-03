# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0015_auto_20150819_0238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['sort'], 'verbose_name': '\u5206\u7c7b(Category)', 'verbose_name_plural': 'Blog \u5206\u7c7b (Categorys)'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['publish_date'], 'verbose_name': '\u6587\u7ae0(Post)', 'verbose_name_plural': 'Blog \u6587\u7ae0 (Posts)'},
        ),
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ('created',), 'verbose_name_plural': 'Snippets (Rest Demo)'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u6807\u7b7e(Tag)', 'verbose_name_plural': 'Blog \u6807\u7b7e(Tags)'},
        ),
        migrations.AddField(
            model_name='post',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='\u5ba1\u6838'),
        ),
    ]
