# Generated by Django 4.1 on 2023-04-27 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_delete_articulo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dataset',
        ),
    ]
