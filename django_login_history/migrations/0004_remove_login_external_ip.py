# Generated by Django 4.0.5 on 2022-06-29 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_login_history', '0003_login_external_ip_alter_login_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='external_ip',
        ),
    ]