# Generated by Django 3.1.4 on 2021-01-13 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0029_auto_20201218_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='activecampaignacademy',
            name='event_attendancy_automation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='marketing.automation'),
        ),
    ]
