"""
Models for Dee Dee core.
"""

from datetime import datetime, timedelta, date, timezone
import uuid

from django.db import models


class DDModel(models.Model):
    """
    A model in Dee Dee.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Asset(DDModel):
    """
    Represents a digital asset (a downloadable file.)
    """

    asset_file = models.FileField(upload_to="assets")
    label = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"{self.label} ({self.id})"


class Bundle(DDModel):
    """
    A SKU. Comes with one or more entitlements.
    """

    label = models.CharField(blank=True, max_length=100)
    available = models.BooleanField(default=True)

    def grant_entitlements(self, recipient_email):
        """
        Grants recipient all associated entitlements. Called on bundle
        purchase fulfillment.
        """
        return [
            ent_policy.grant_entitlement(recipient_email)
            for ent_policy in self.entitlement_policies.all()
        ]

    def __str__(self):
        return f"{self.label} ({self.id})"


class EntitlementPolicy(DDModel):
    """
    An entitlement that is granted with a bundle. This is the policy that
    creates recipient specific entitlements.
    """

    bundle = models.ForeignKey(
        Bundle, related_name="entitlement_policies", on_delete=models.CASCADE
    )
    assets = models.ManyToManyField(Asset, related_name="entitlement_policies")
    token_allowance_policy = models.IntegerField(default=1)
    expire_after = models.IntegerField(blank=True, null=True)
    label = models.CharField(blank=True, max_length=100)

    def grant_entitlement(self, recipient_email):
        """
        Creates an entitlement for the recipient email.  Called on bundle purchase.
        """
        expiry_date = (
            date.today() + timedelta(days=self.expire_after)
            if self.expire_after
            else None
        )
        ent = Entitlement.objects.create(
            token_allowance=self.token_allowance_policy,
            recipient=recipient_email,
            expiry=expiry_date,
            source_policy=self,
        )
        for asset in self.assets.all():
            ent.assets.add(asset)
        ent.save()
        return ent

    def __str__(self):
        return f"{self.label} ({self.id})"


class Entitlement(DDModel):
    """
    An entitlement granted to a user to create one or more download tokens.
    """

    assets = models.ManyToManyField(Asset, related_name="entitlements")
    token_allowance = models.IntegerField(default=1)
    recipient = models.EmailField()  # the grantee of the entitlement
    source_policy = models.ForeignKey(
        EntitlementPolicy,
        null=True,
        related_name="entitlements",
        on_delete=models.SET_NULL,
    )
    expiry = models.DateField(null=True)

    def has_more_tokens(self):
        """
        Returns true if this entitlement can create more tokens.
        """
        return self.token_allowance > 0

    def create_token(self):
        """
        Creates the download token.
        """
        if not self.has_more_tokens():
            raise Entitlement.AllowanceExceeded

        token = Token.objects.create(
            source_entitlement=self,
        )
        for asset in self.assets.all():
            token.assets.add(asset)

        token.save()
        self.token_allowance -= 1
        self.save()
        return token

    class AllowanceExceeded(Exception):
        """
        INdicates the token allowance has been exceeded for this entitlement.
        """


class Token(DDModel):
    """
    Token to create a download session.
    """

    used = models.BooleanField(default=False)
    assets = models.ManyToManyField(Asset, related_name="tokens")
    source_entitlement = models.ForeignKey(
        Entitlement, related_name="created_tokens", on_delete=models.CASCADE
    )

    def create_session(self):
        """
        Creates the session from this token.
        """
        if self.used:
            raise Token.Expired()

        session = DownloadSession.objects.create(
            token=self,
            created=datetime.now(timezone.utc),
        )
        for asset in self.assets.all():
            session.assets.add(asset)
        session.save()
        self.used = True
        self.save()

        return session

    class Expired(Exception):
        """
        Indicates token has expired
        """


class DownloadSession(DDModel):
    """
    Represents a temporary download session that grants access to
    one or more assets.
    """

    assets = models.ManyToManyField(Asset, related_name="download_sessions")
    created = models.DateTimeField(blank=True, default=datetime.now)
    ttl = models.IntegerField(default=5)  # 5 minute TTL default
    token = models.OneToOneField(
        Token, related_name="download_session", on_delete=models.CASCADE
    )

    def is_valid(self):
        """
        Returns true if the session is still alive, false if it has expired.
        """
        return datetime.now(timezone.utc) < self.created + timedelta(minutes=self.ttl)
