# Generated by Django 3.2.4 on 2021-06-28 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20210622_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment_coumt',
        ),
    ]
