# Generated by Django 3.0.6 on 2020-07-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sidebar',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '显示'), (0, '隐藏')], default=1, verbose_name='状态'),
        ),
    ]