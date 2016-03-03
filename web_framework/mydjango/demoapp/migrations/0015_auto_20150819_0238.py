# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demoapp', '0014_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='highlighted',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='snippet',
            name='owner',
            field=models.ForeignKey(related_name='snippets', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
