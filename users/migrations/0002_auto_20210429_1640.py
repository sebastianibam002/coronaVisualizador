# Generated by Django 3.2 on 2021-04-29 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='afiliado',
            name='is_okay',
        ),
        migrations.AddField(
            model_name='afiliado',
            name='state',
            field=models.CharField(default=True, max_length=2),
            preserve_default=False,
        ),
    ]
