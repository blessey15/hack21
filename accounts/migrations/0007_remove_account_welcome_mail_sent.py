# Generated by Django 3.0.6 on 2020-11-30 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_account_welcome_mail_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='welcome_mail_sent',
        ),
    ]