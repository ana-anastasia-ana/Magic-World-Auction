# Generated by Django 4.1.5 on 2023-11-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_alter_category_id_alter_listing_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]