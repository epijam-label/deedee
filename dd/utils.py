"""
Utils for DD
"""

import base64
import hashlib
import hmac
import logging

from django.conf import settings


log = logging.getLogger(__file__)


def verify_shopify_webhook(request):
    """
    Verfies the request as a genuine shopify webhook.
    """
    log.debug("Debugging verify_shopify_webhook")
    shopify_hmac_header = request.META.get(settings.SHOPIFY_HMAC_HEADER)
    log.debug(f"hmac header is: {shopify_hmac_header}")
    encoded_secret = settings.SHOPIFY_API_SECRET.encode("utf-8")
    log.debug(f"encoded secret is: {encoded_secret}")
    digest = hmac.new(
        encoded_secret,
        request.body,
        digestmod=hashlib.sha256,
    ).digest()
    computed_hmac = base64.b64encode(digest)
    return hmac.compare_digest(computed_hmac, shopify_hmac_header.encode("utf-8"))
