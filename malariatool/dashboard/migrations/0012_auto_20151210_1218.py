# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20151210_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='sub_tasks',
        ),
        migrations.AddField(
            model_name='item',
            name='task',
            field=models.ForeignKey(related_name='taskitems', default=None, to='dashboard.Task'),
            preserve_default=False,
        ),
    ]
