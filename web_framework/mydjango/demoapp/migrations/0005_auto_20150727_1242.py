# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demoapp', '0004_auto_20150727_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('alias', models.CharField(max_length=100, verbose_name=b'\xe5\x88\xab\xe5\x90\x8d')),
                ('sort', models.SmallIntegerField(verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f')),
            ],
            options={
                'ordering': ['sort'],
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('content', models.TextField(verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9')),
                ('excerpt', models.TextField(verbose_name=b'\xe6\x91\x98\xe8\xa6\x81')),
                ('publish_date', models.DateTimeField(verbose_name=b'\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xb6\xe9\x97\xb4')),
                ('status', models.IntegerField(default=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(1, b'\xe5\x8f\x91\xe5\xb8\x83'), (2, b'\xe8\x8d\x89\xe7\xa8\xbf\xe7\xae\xb1')])),
                ('comments_count', models.IntegerField(default=0, editable=False)),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('alias', models.CharField(max_length=100, verbose_name=b'\xe5\x88\xab\xe5\x90\x8d', blank=True)),
                ('keywords', models.CharField(max_length=500, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97', blank=True)),
                ('description', models.TextField(verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('categories', models.ManyToManyField(related_name='posts', verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', to='demoapp.Category', blank=True)),
                ('user', models.ForeignKey(related_name='posts', verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['publish_date'],
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagname', models.CharField(max_length=60, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe5\x90\x8d')),
                ('post_ids', models.TextField(editable=False)),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['sort'], 'verbose_name': '\u9009\u9879', 'verbose_name_plural': '\u9009\u9879'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u6295\u7968\u95ee\u9898', 'verbose_name_plural': '\u6295\u7968\u95ee\u9898'},
        ),
    ]
