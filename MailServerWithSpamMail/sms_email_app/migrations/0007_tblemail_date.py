# Generated by Django 4.2.7 on 2024-03-19 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_email_app', '0006_tblemail_secretkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblemail',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
