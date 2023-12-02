# Generated by Django 4.1.5 on 2023-12-01 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0011_alter_bid_id_alter_category_id_alter_comment_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]