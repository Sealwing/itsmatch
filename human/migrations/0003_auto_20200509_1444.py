# Generated by Django 3.0.6 on 2020-05-09 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human', '0002_auto_20200509_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='avatar',
            field=models.ImageField(default='S:\\development\\itsmatch\\human\\static\\avatars\\cat_default.bmp', upload_to='S:\\development\\itsmatch\\human\\static\\avatars'),
        ),
    ]