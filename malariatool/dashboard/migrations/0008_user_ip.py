# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20151203_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip',
            field=models.ForeignKey(related_name='ip_user', default=None, to='dashboard.IP'),
            preserve_default=False,
        ),
    ]
