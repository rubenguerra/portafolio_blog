# Generated by Django 4.1 on 2023-02-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_comentario_estado_comentario_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
