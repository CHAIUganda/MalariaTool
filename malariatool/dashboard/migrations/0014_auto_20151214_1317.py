# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20151214_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='task',
        ),
        migrations.AddField(
            model_name='note',
            name='item',
            field=models.ForeignKey(related_name='taskitemnotes', default=None, to='dashboard.Item'),
            preserve_default=False,
        ),
    ]
