# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20151216_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='ip',
            field=models.ForeignKey(related_name='meetings', default=1, to='dashboard.IP'),
            preserve_default=False,
        ),
    ]
