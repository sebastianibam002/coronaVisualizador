# Generated by Django 3.2 on 2021-04-29 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.IntegerField()),
                ('is_okay', models.BooleanField()),
            ],
        ),
    ]
