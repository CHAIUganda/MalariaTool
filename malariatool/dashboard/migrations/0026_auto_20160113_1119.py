# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='profile_url',
            new_name='profile_picture',
        ),
    ]
