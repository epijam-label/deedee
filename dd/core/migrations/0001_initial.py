# Generated by Django 5.0.7 on 2024-07-29 18:47

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("asset_file", models.FileField(upload_to="assets")),
                ("label", models.CharField(blank=True, max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Bundle",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=100)),
                ("available", models.BooleanField(default=True)),
                ("token_allowance_policy", models.IntegerField(default=1)),
                ("expire_after", models.IntegerField(blank=True, null=True)),
                (
                    "assets",
                    models.ManyToManyField(related_name="bundles", to="core.asset"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DownloadCard",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email_capture_required", models.BooleanField(default=False)),
                ("recipient_email", models.EmailField(max_length=254, null=True)),
                ("used", models.BooleanField(default=False)),
                (
                    "bundle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="download_cards",
                        to="core.bundle",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Entitlement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("token_allowance", models.IntegerField(default=1)),
                ("recipient", models.EmailField(max_length=254)),
                ("expiry", models.DateField(null=True)),
                (
                    "assets",
                    models.ManyToManyField(
                        related_name="entitlements", to="core.asset"
                    ),
                ),
                (
                    "source_bundle",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="entitlements",
                        to="core.bundle",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("used", models.BooleanField(default=False)),
                (
                    "assets",
                    models.ManyToManyField(related_name="tokens", to="core.asset"),
                ),
                (
                    "source_entitlement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_tokens",
                        to="core.entitlement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DownloadSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("ttl", models.IntegerField(default=5)),
                (
                    "assets",
                    models.ManyToManyField(
                        related_name="download_sessions", to="core.asset"
                    ),
                ),
                (
                    "token",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="download_session",
                        to="core.token",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
