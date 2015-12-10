# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_user_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ip',
            field=models.ForeignKey(related_name='ip_user', blank=True, to='dashboard.IP', null=True),
        ),
    ]
