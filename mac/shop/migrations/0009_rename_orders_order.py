# Generated by Django 4.1.7 on 2023-07-02 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_orders'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
