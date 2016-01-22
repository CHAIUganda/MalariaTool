# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_auto_20160113_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(max_length=150, choices=[(b'not_started', b'Not Started'), (b'ongoing', b'Ongoing'), (b'Done', b'Done')]),
        ),
    ]
