# Generated by Django 4.2.7 on 2024-01-09 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms_email_app', '0004_tblspam'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblspam',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_email', to='sms_email_app.tbluser'),
        ),
    ]
