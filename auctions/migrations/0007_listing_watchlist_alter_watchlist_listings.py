# Generated by Django 4.1.5 on 2023-11-29 21:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_alter_category_id_alter_listing_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="listingWatchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="listings",
            field=models.ManyToManyField(
                blank=True, related_name="watchlists", to="auctions.listing"
            ),
        ),
    ]
