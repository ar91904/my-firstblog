# Generated by Django 3.2.20 on 2023-07-20 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text1',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=250),
        ),
    ]
