# Generated by Django 5.0.1 on 2024-01-18 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_group_membership_group_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]