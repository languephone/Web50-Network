# Generated by Django 3.2.5 on 2021-07-19 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ManyToManyField(blank=True, to='network.Post'),
        ),
    ]
